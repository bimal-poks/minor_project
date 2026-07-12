import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import StudentManagement from './pages/StudentManagement';
import LiveAttendance from './pages/LiveAttendance';
import SessionManagement from './pages/SessionManagement';

function App() {
  const [page, setPage] = useState('dashboard');
  const [activeSession, setActiveSession] = useState(null);

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
      <nav className="bg-white border-b px-6 py-3 flex gap-4 items-center">
        {navButton('dashboard', 'Dashboard')}
        {navButton('attendance', 'Live Attendance')}
        {navButton('students', 'Students')}
        {navButton('sessions', 'Sessions')}
        {activeSession && (
          <span className="ml-auto text-sm text-blue-600 font-medium">
            Active: {activeSession.name}
          </span>
        )}
      </nav>

      {page === 'dashboard' && <Dashboard />}
      {page === 'attendance' && <LiveAttendance />}
      {page === 'students' && <StudentManagement />}
      {page === 'sessions' && (
        <SessionManagement onSessionSelect={setActiveSession} />
      )}
    </div>
  );
}

export default App;