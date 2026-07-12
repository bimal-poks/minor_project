import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import StudentManagement from './pages/StudentManagement';
import LiveAttendance from './pages/LiveAttendance';
import SessionManagement from './pages/SessionManagement';

const navItems = [
  { id: 'dashboard', label: '📊 Dashboard' },
  { id: 'attendance', label: '🎥 Live Attendance' },
  { id: 'students', label: '👥 Students' },
  { id: 'sessions', label: '📅 Sessions' },
];

function App() {
  const [page, setPage] = useState('dashboard');
  const [activeSession, setActiveSession] = useState(null);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">

      {/* Top Header */}
      <header className="bg-blue-700 text-white px-6 py-4 flex items-center justify-between shadow">
        <div>
          <h1 className="text-xl font-bold tracking-wide">
            Smart Attendance System
          </h1>
          <p className="text-blue-200 text-xs mt-0.5">
            Pulchowk Campus — Dept. of Electronics & Computer Engineering
          </p>
        </div>
        {activeSession && (
          <div className="text-right">
            <div className="text-xs text-blue-200">Active Session</div>
            <div className="text-sm font-semibold">{activeSession.name}</div>
            <div className="text-xs text-blue-200">{activeSession.date}</div>
          </div>
        )}
      </header>

      <div className="flex flex-1">

        {/* Sidebar */}
        <aside className="w-52 bg-white border-r shadow-sm flex flex-col py-4">
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setPage(item.id)}
              className={`text-left px-5 py-3 text-sm font-medium transition
                ${page === item.id
                  ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700'
                  : 'text-gray-600 hover:bg-gray-50'
                }`}
            >
              {item.label}
            </button>
          ))}
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto">
          {page === 'dashboard' && <Dashboard />}
          {page === 'attendance' && <LiveAttendance />}
          {page === 'students' && <StudentManagement />}
          {page === 'sessions' && (
            <SessionManagement onSessionSelect={setActiveSession} />
          )}
        </main>

      </div>
    </div>
  );
}

export default App;