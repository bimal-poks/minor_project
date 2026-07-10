import csv
import pickle
import os
from django.core.management.base import BaseCommand
from attendance.models import Student, FaceEmbedding

ROSTER_PATH = os.path.join("..", "face_modules", "dataset", "roster.csv")
EMBEDDINGS_PATH = os.path.join("..", "face_modules", "embeddings", "face_db.pkl")

class Command(BaseCommand):
    help = "Import students from roster.csv and embeddings from face_db.pkl"

    def handle(self, *args, **options):
        # Load embeddings
        with open(EMBEDDINGS_PATH, "rb") as f:
            embeddings_db = pickle.load(f)

        # Load roster and create students
        with open(ROSTER_PATH, newline='') as f:
            reader = csv.DictReader(f)
            created_count = 0
            embedded_count = 0

            for row in reader:
                roll_number = row["roll_number"].strip()
                name = row["name"].strip()

                student, created = Student.objects.get_or_create(
                    roll_number=roll_number,
                    defaults={"name": name}
                )
                if created:
                    created_count += 1

                if roll_number in embeddings_db:
                    vector = embeddings_db[roll_number].tolist()
                    FaceEmbedding.objects.update_or_create(
                        student=student,
                        defaults={"vector": vector}
                    )
                    embedded_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_count} new students. Added embeddings for {embedded_count} students."
        ))