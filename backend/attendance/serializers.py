from rest_framework import serializers
from .models import Student, FaceEmbedding, Session, AttendanceRecord


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'roll_number', 'name', 'created_at']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'date', 'start_time', 'end_time']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_name', 'student_roll',
                  'session', 'session_name', 'timestamp', 'status']