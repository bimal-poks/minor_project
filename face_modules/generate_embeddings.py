import cv2
import os
import numpy as np
import pickle
from insightface.app import FaceAnalysis

DATASET_DIR = "dataset/raw"
TRAIN_COUNT = 3  # use first 3 photos for embedding, last 2 for testing

def load_model():
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app

def generate_embeddings(app, dataset_dir=DATASET_DIR):
    embeddings_db = {}

    for roll_number in os.listdir(dataset_dir):
        student_folder = os.path.join(dataset_dir, roll_number)
        if not os.path.isdir(student_folder):
            continue

        all_images = sorted([
            f for f in os.listdir(student_folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

        # use only first TRAIN_COUNT images for embedding
        train_images = all_images[:TRAIN_COUNT]
        print(f"{roll_number}: using {train_images} for embedding")

        student_embeddings = []
        for filename in train_images:
            image_path = os.path.join(student_folder, filename)
            img = cv2.imread(image_path)
            if img is None:
                continue

            faces = app.get(img)
            if len(faces) == 1:
                student_embeddings.append(faces[0].embedding)
            else:
                print(f"  Skipping {filename}: {len(faces)} faces detected")

        if student_embeddings:
            avg_embedding = np.mean(student_embeddings, axis=0)
            embeddings_db[roll_number] = avg_embedding
            print(f"  → Embedding generated from {len(student_embeddings)} photo(s)")

    return embeddings_db

if __name__ == "__main__":
    app = load_model()
    db = generate_embeddings(app)

    os.makedirs("embeddings", exist_ok=True)
    with open("embeddings/face_db.pkl", "wb") as f:
        pickle.dump(db, f)

    print(f"\nSaved {len(db)} student embeddings to embeddings/face_db.pkl")
    print(f"NOTE: Embeddings built from first {TRAIN_COUNT} photos only.")
    print(f"Last 2 photos per student are held out for evaluation.")