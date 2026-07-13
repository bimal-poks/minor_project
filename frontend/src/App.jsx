import { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import StudentManagement from './pages/StudentManagement';
import LiveAttendance from './pages/LiveAttendance';
import SessionManagement from './pages/SessionManagement';
import Login from './pages/Login';

const navItems = [
  { id: 'dashboard', label: '📊 Dashboard' },
  { id: 'attendance', label: '🎥 Live Attendance' },
  { id: 'students', label: '👥 Students' },
  { id: 'sessions', label: '📅 Sessions' },
];

function App() {
  const [page, setPage] = useState('dashboard');
  const [activeSession, setActiveSession] = useState(null);
  const [username, setUsername] = useState(null);

  useEffect(() => {
    const savedUsername = localStorage.getItem('username');
    const savedToken = localStorage.getItem('token');
    if (savedUsername && savedToken) {
      setUsername(savedUsername);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUsername(null);
  };

  if (!username) {
    return <Login onLoginSuccess={setUsername} />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-700 text-white px-6 py-4 flex items-center justify-between shadow">
        <div>
          <h1 className="text-xl font-bold tracking-wide">Smart Attendance System</h1>
          <p className="text-blue-200 text-xs mt-0.5">
            Pulchowk Campus — Dept. of Electronics & Computer Engineering
          </p>
        </div>
        <div className="flex items-center gap-4">
          {activeSession && (
            <div className="text-right">
              <div className="text-xs text-blue-200">Active Session</div>
              <div className="text-sm font-semibold">{activeSession.name}</div>
            </div>
          )}
          <div className="text-right">
            <div className="text-sm">{username}</div>
            <button onClick={handleLogout} className="text-xs text-blue-200 hover:text-white underline">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
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

        <main className="flex-1 overflow-auto">
          {page === 'dashboard' && <Dashboard />}
          {page === 'attendance' && <LiveAttendance />}
          {page === 'students' && <StudentManagement />}
          {page === 'sessions' && <SessionManagement onSessionSelect={setActiveSession} />}
        </main>
      </div>
    </div>
  );
}

export default App;