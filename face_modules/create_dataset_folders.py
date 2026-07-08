import csv
import os

ROSTER_PATH = "dataset/roster.csv"
DATASET_DIR = "dataset/raw"

def create_folders():
    os.makedirs(DATASET_DIR, exist_ok=True)

    with open(ROSTER_PATH, newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            roll_number = row["roll_number"].strip()
            folder_path = os.path.join(DATASET_DIR, roll_number)
            os.makedirs(folder_path, exist_ok=True)
            count += 1

    print(f"Created/verified {count} student folders in {DATASET_DIR}")

if __name__ == "__main__":
    create_folders()