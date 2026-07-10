from django.db import models

class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class FaceEmbedding(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="embedding")
    vector = models.JSONField()  # stores the 512-dim embedding as a list
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding for {self.student.roll_number}"


class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date}"


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="attendance_records")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="present")

    class Meta:
        unique_together = ("student", "session")

    def __str__(self):
        return f"{self.student.roll_number} - {self.session.name} - {self.status}"