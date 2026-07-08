# API Endpoints

## Students
GET    /api/students/          - list all students
POST   /api/students/          - add new student (name, roll number, photo)
GET    /api/students/<id>/     - get one student's detail
PATCH  /api/students/<id>/     - update student info
DELETE /api/students/<id>/     - remove a student

## Attendance
POST   /api/attendance/mark/       - mark attendance (called after face match)
  - input: student_id (or roll_number), session_id, timestamp
  - output: success/failure, duplicate check result

GET    /api/attendance/report/     - filterable report
  - query params: date, session_id, student_id (optional)

GET    /api/attendance/today/      - today's summary (for dashboard cards)

## Auth
POST   /api/auth/login/        - teacher/admin login
POST   /api/auth/logout/