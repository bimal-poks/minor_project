import cv2
import pickle
import numpy as np
import requests
import time
from collections import deque
from insightface.app import FaceAnalysis

THRESHOLD = 0.55
SESSION_ID = 1
API_URL = "http://127.0.0.1:8000/api/attendance/mark/"
COOLDOWN_SECONDS = 10

LIVENESS_WINDOW = 2.0      # seconds of tracking before deciding liveness
MIN_MOVEMENT_PX = 2        # minimum bbox-center movement to count as "alive"
MIN_SAMPLES = 8             # minimum frames needed before judging liveness

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

def mark_attendance(roll_number):
    try:
        response = requests.post(API_URL, json={
            "roll_number": roll_number,
            "session_id": SESSION_ID
        })
        data = response.json()
        print(f"API response: {data.get('message', data)}")
    except requests.exceptions.ConnectionError:
        print("Could not reach backend - is Django running?")

def check_liveness(track_buffer):
    """Returns True if enough natural movement is seen in the tracked positions."""
    if len(track_buffer) < MIN_SAMPLES:
        return False, 0

    xs = [p[0] for p in track_buffer]
    ys = [p[1] for p in track_buffer]
    movement = max(max(xs) - min(xs), max(ys) - min(ys))
    return movement >= MIN_MOVEMENT_PX, movement

def run_live_recognition():
    app = load_model()
    db = load_embeddings_db()
    cap = cv2.VideoCapture(0)

    last_marked = {}
    tracking = {}  # roll_number -> deque of (center_x, center_y, timestamp)

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

                # drop samples older than the liveness window
                while tracking[match] and now - tracking[match][0][2] > LIVENESS_WINDOW:
                    tracking[match].popleft()

                is_live, movement = check_liveness(tracking[match])

                if not is_live:
                    label = f"{match} - verifying liveness..."
                    color = (0, 165, 255)  # orange
                else:
                    label = f"{match} ({score:.2f}) LIVE"
                    color = (0, 255, 0)

                    if match not in last_marked or (now - last_marked[match]) > COOLDOWN_SECONDS:
                        mark_attendance(match)
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