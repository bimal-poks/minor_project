# Smart Attendance System
BE Minor Project — Pulchowk Campus, Dept. of Electronics & Computer Engineering

## Team
- Amit Acharya
- Anish Khadka
- Bimal Pokharel

## Tech Stack
- Frontend: React.js + Tailwind
- Backend: Django + DRF
- Face Recognition: OpenCV + InsightFace (RetinaFace + ArcFace)
- Database: SQLite (dev) / PostgreSQL (prod)


## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/bimal-poks/smart-attendance-system.git
cd smart-attendance-system/minor_project
```

### 2. Face Recognition Module Setup
```bash
cd face_modules
python -m venv venv
venv\Scripts\activate          

pip install -r requirements.txt
```

### 3. Backend Setup (Django)
```bash
cd ../backend
python -m venv venv
venv\Scripts\activate         

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Backend runs at `http://127.0.0.1:8000`

### 4. Frontend Setup (React)
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`

### 5. Import Student Data
Place student photos in `face_modules/dataset/raw/<roll_number>/` (5 photos per student), and fill in `face_modules/dataset/roster.csv` with roll numbers and names. Then:
```bash
cd face_modules
venv\Scripts\activate
python create_dataset_folders.py
python generate_embeddings.py

cd ../backend
venv\Scripts\activate
python manage.py import_students
```

### 6. Running Live Attendance
With the backend running and a session created for today's date (via the Sessions tab in the frontend, or Django admin):
```bash
cd face_modules
venv\Scripts\activate
python recognize.py
```
The script automatically detects today's session and marks attendance for recognized, verified-live faces. Results appear live in the frontend Dashboard and Live Attendance pages.

### Login
Use the Django superuser credentials created in Step 3 to log into the web dashboard.
