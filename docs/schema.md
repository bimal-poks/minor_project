# Database Schema

## Student
- id (PK, auto)
- roll_number (unique, string)
- name (string)
- created_at (datetime)

## FaceEmbedding
- id (PK, auto)
- student (FK -> Student)
- embedding (JSON or binary field - stores the 512-dim ArcFace vector)
- created_at (datetime)

## Session
- id (PK, auto)
- name (string, e.g. "CT Lecture - Sec A")
- date (date)
- start_time (time)
- end_time (time)

## AttendanceRecord
- id (PK, auto)
- student (FK -> Student)
- session (FK -> Session)
- timestamp (datetime)
- status (string, e.g. "present")

# unique_together: (student, session) - prevents duplicate marks per session