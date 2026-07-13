import cv2
import pickle
import numpy as np
import requests
import time
from datetime import date
from collections import deque
from insightface.app import FaceAnalysis

THRESHOLD = 0.55
API_BASE = "http://127.0.0.1:8000/api"
COOLDOWN_SECONDS = 10
LIVENESS_WINDOW = 2.0
MIN_MOVEMENT_PX = 2
MIN_SAMPLES = 8
LIVENESS_LOCK_SECONDS = 5.0

def get_today_session():
    """Fetch today's session automatically. If multiple exist, use the most recent."""
    try:
        response = requests.get(f"{API_BASE}/sessions/")
        sessions = response.json()
        today_str = str(date.today())

        todays_sessions = [s for s in sessions if s['date'] == today_str]

        if not todays_sessions:
            print(f"No session found for today ({today_str}). Create one via the frontend first.")
            return None

        # use the most recently created one (highest id) if multiple exist today
        chosen = max(todays_sessions, key=lambda s: s['id'])
        print(f"Using session: '{chosen['name']}' (ID: {chosen['id']}, {chosen['date']})")
        return chosen['id']

    except requests.exceptions.ConnectionError:
        print("Could not reach backend - is Django running?")
        return None

def load_model():
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app

def load_embeddings_db(path="embeddings/face_db.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_best_match(embedding, db):
    best_match = None
    best_score = -1
    for roll_number, stored_embedding in db.items():
        score = cosine_similarity(embedding, stored_embedding)
        if score > best_score:
            best_score = score
            best_match = roll_number
    if best_score >= THRESHOLD:
        return best_match, best_score
    return None, best_score

def mark_attendance(roll_number, session_id):
    try:
        response = requests.post(f"{API_BASE}/attendance/mark/", json={
            "roll_number": roll_number,
            "session_id": session_id
        })
        data = response.json()
        print(f"API response: {data.get('message', data)}")
    except requests.exceptions.ConnectionError:
        print("Could not reach backend - is Django running?")

def check_liveness(track_buffer):
    if len(track_buffer) < MIN_SAMPLES:
        return False, 0
    xs = [p[0] for p in track_buffer]
    ys = [p[1] for p in track_buffer]
    movement = max(max(xs) - min(xs), max(ys) - min(ys))
    return movement >= MIN_MOVEMENT_PX, movement

def run_live_recognition():
    session_id = get_today_session()
    if session_id is None:
        return  # stop here, nothing to mark attendance against

    app = load_model()
    db = load_embeddings_db()
    cap = cv2.VideoCapture(0)

    last_marked = {}
    tracking = {}
    liveness_confirmed = {}

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)
        now = time.time()

        for face in faces:
            box = face.bbox.astype(int)
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            match, score = find_best_match(face.embedding, db)

            if match:
                if match not in tracking:
                    tracking[match] = deque()
                tracking[match].append((center[0], center[1], now))

                while tracking[match] and now - tracking[match][0][2] > LIVENESS_WINDOW:
                    tracking[match].popleft()

                already_confirmed = (
                    match in liveness_confirmed and
                    now - liveness_confirmed[match] < LIVENESS_LOCK_SECONDS
                )

                if not already_confirmed:
                    is_live, movement = check_liveness(tracking[match])
                    if is_live:
                        liveness_confirmed[match] = now
                        already_confirmed = True

                if not already_confirmed:
                    label = f"{match} - verifying liveness..."
                    color = (0, 165, 255)
                else:
                    label = f"{match} ({score:.2f}) LIVE"
                    color = (0, 255, 0)

                    if match not in last_marked or (now - last_marked[match]) > COOLDOWN_SECONDS:
                        mark_attendance(match, session_id)
                        last_marked[match] = now
            else:
                label = f"Unknown ({score:.2f})"
                color = (0, 0, 255)

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Live Recognition + Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_live_recognition()