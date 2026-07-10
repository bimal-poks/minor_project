import { useState } from 'react';
import StudentManagement from './pages/StudentManagement';
import LiveAttendance from './pages/LiveAttendance';

function App() {
  const [page, setPage] = useState('attendance');

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex gap-4">
        <button
          onClick={() => setPage('attendance')}
          className={`px-3 py-1 rounded ${page === 'attendance' ? 'bg-blue-600 text-white' : 'text-gray-600'}`}
        >
          Live Attendance
        </button>
        <button
          onClick={() => setPage('students')}
          className={`px-3 py-1 rounded ${page === 'students' ? 'bg-blue-600 text-white' : 'text-gray-600'}`}
        >
          Students
        </button>
      </nav>

      {page === 'attendance' ? <LiveAttendance /> : <StudentManagement />}
    </div>
  );
}

export default App;