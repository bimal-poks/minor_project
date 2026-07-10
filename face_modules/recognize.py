import cv2
import pickle
import numpy as np
from insightface.app import FaceAnalysis

THRESHOLD = 0.4  # similarity threshold - tune this based on testing

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

def run_live_recognition():
    app = load_model()
    db = load_embeddings_db()
    cap = cv2.VideoCapture(0)

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)

        for face in faces:
            box = face.bbox.astype(int)
            match, score = find_best_match(face.embedding, db)

            if match:
                label = f"{match} ({score:.2f})"
                color = (0, 255, 0)
            else:
                label = f"Unknown ({score:.2f})"
                color = (0, 0, 255)

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Live Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_live_recognition()