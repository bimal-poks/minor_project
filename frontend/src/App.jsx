import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import StudentManagement from './pages/StudentManagement';
import LiveAttendance from './pages/LiveAttendance';

function App() {
  const [page, setPage] = useState('dashboard');

  const navButton = (id, label) => (
    <button
      onClick={() => setPage(id)}
      className={`px-3 py-1 rounded ${page === id ? 'bg-blue-600 text-white' : 'text-gray-600'}`}
    >
      {label}
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex gap-4">
        {navButton('dashboard', 'Dashboard')}
        {navButton('attendance', 'Live Attendance')}
        {navButton('students', 'Students')}
      </nav>

      {page === 'dashboard' && <Dashboard />}
      {page === 'attendance' && <LiveAttendance />}
      {page === 'students' && <StudentManagement />}
    </div>
  );
}

export default App;