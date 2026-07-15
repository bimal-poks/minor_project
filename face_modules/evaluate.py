import cv2
import os
import pickle
import numpy as np
import time
from insightface.app import FaceAnalysis

EMBEDDINGS_PATH = "embeddings/face_db.pkl"
DATASET_DIR     = "dataset/raw"
THRESHOLD       = 0.55
TRAIN_COUNT     = 3  # must match generate_embeddings.py

def load_model():
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app

def load_embeddings_db():
    with open(EMBEDDINGS_PATH, "rb") as f:
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

def evaluate():
    print("Loading model...")
    app = load_model()
    db  = load_embeddings_db()

    true_positives   = 0
    false_rejections = 0
    false_accepts    = 0
    total_attempts   = 0
    processing_times = []
    per_student      = {}

    print(f"\nEvaluating on HELD-OUT photos (photos {TRAIN_COUNT+1} and {TRAIN_COUNT+2} per student)")
    print(f"Students in database : {len(db)}")
    print(f"Threshold            : {THRESHOLD}")
    print("-" * 60)

    for true_roll in sorted(os.listdir(DATASET_DIR)):
        student_folder = os.path.join(DATASET_DIR, true_roll)
        if not os.path.isdir(student_folder):
            continue

        all_images = sorted([
            f for f in os.listdir(student_folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        # test on held-out images only (everything after TRAIN_COUNT)
        test_images = all_images[TRAIN_COUNT:]

        if not test_images:
            print(f"  {true_roll}: no held-out images — skipping")
            continue

        per_student[true_roll] = {'attempts': 0, 'correct': 0, 'scores': []}

        for img_file in test_images:
            img_path = os.path.join(student_folder, img_file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            start_time = time.time()
            faces = app.get(img)
            elapsed = (time.time() - start_time) * 1000
            processing_times.append(elapsed)

            total_attempts += 1
            per_student[true_roll]['attempts'] += 1

            if not faces:
                false_rejections += 1
                print(f"  {true_roll}/{img_file}: NO FACE DETECTED → FRR")
                continue

            predicted_roll, score = find_best_match(faces[0].embedding, db)
            per_student[true_roll]['scores'].append(score)

            if predicted_roll is None:
                false_rejections += 1
                print(f"  {true_roll}/{img_file}: score={score:.3f} → REJECTED (FRR)")
            elif predicted_roll == true_roll:
                true_positives += 1
                per_student[true_roll]['correct'] += 1
                print(f"  {true_roll}/{img_file}: score={score:.3f} → CORRECT ✓")
            else:
                false_accepts += 1
                print(f"  {true_roll}/{img_file}: score={score:.3f} → WRONG: {predicted_roll} (FAR)")

    # ── Results ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS (Hold-out Test Set)")
    print("=" * 60)

    accuracy = (true_positives   / total_attempts * 100) if total_attempts > 0 else 0
    far      = (false_accepts    / total_attempts * 100) if total_attempts > 0 else 0
    frr      = (false_rejections / total_attempts * 100) if total_attempts > 0 else 0
    avg_time = np.mean(processing_times) if processing_times else 0

    print(f"Total test images       : {total_attempts}")
    print(f"True Positives          : {true_positives}")
    print(f"False Rejections (FRR)  : {false_rejections}")
    print(f"False Acceptances (FAR) : {false_accepts}")
    print(f"\nRecognition Accuracy    : {accuracy:.2f}%")
    print(f"False Rejection Rate    : {frr:.2f}%")
    print(f"False Acceptance Rate   : {far:.2f}%")
    print(f"\nAvg Processing Time     : {avg_time:.1f} ms/image")
    print(f"Min Processing Time     : {min(processing_times):.1f} ms")
    print(f"Max Processing Time     : {max(processing_times):.1f} ms")

    print("\nPer-Student Accuracy:")
    print("-" * 40)
    for roll, data in sorted(per_student.items()):
        acc = (data['correct'] / data['attempts'] * 100) if data['attempts'] > 0 else 0
        avg_score = np.mean(data['scores']) if data['scores'] else 0
        print(f"  {roll}: {data['correct']}/{data['attempts']} correct "
              f"({acc:.0f}%) | avg score: {avg_score:.3f}")

    print("\n" + "=" * 60)
    print("Evaluation method: 3-photo training / 2-photo hold-out split")
    print("FAR tested on known students only — imposter testing")
    print("recommended for comprehensive real-world FAR assessment.")
    print("=" * 60)

    return {
        'accuracy': accuracy,
        'far': far,
        'frr': frr,
        'avg_processing_time_ms': avg_time,
    }

if __name__ == "__main__":
    results = evaluate()