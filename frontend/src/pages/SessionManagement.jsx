import { useState, useEffect } from 'react';
import api from '../api';

function SessionManagement({ onSessionSelect }) {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // form state
  const [name, setName] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState(null);

  const fetchSessions = () => {
    setLoading(true);
    api.get('/sessions/')
      .then(response => {
        setSessions(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Could not load sessions');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormError(null);

    if (!name.trim() || !date || !startTime || !endTime) {
      setFormError('All fields are required.');
      return;
    }

    setSubmitting(true);
    api.post('/sessions/', {
      name: name.trim(),
      date: date,
      start_time: startTime,
      end_time: endTime
    })
      .then(response => {
        setName('');
        setStartTime('');
        setEndTime('');
        setSubmitting(false);
        fetchSessions();
        // auto-select the newly created session
        setActiveSession(response.data);
        if (onSessionSelect) onSessionSelect(response.data);
      })
      .catch(err => {
        setFormError('Failed to create session.');
        setSubmitting(false);
      });
  };

  const handleSelect = (session) => {
    setActiveSession(session);
    if (onSessionSelect) onSessionSelect(session);
  };

  if (loading) return <div className="p-6">Loading sessions...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Session Management</h1>

      {/* Create Session Form */}
      <div className="bg-white border rounded-lg p-4 mb-6">
        <h2 className="text-lg font-semibold mb-3">Create New Session</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
          <input
            type="text"
            placeholder="Session name (e.g. CT Lecture - Sec A)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border rounded px-3 py-2 col-span-2"
          />
          <div>
            <label className="text-sm text-gray-500 block mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="border rounded px-3 py-2 w-full"
            />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-sm text-gray-500 block mb-1">Start Time</label>
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="border rounded px-3 py-2 w-full"
              />
            </div>
            <div>
              <label className="text-sm text-gray-500 block mb-1">End Time</label>
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                className="border rounded px-3 py-2 w-full"
              />
            </div>
          </div>
          {formError && (
            <div className="text-red-600 col-span-2 text-sm">{formError}</div>
          )}
          <button
            type="submit"
            disabled={submitting}
            className="bg-blue-600 text-white px-4 py-2 rounded col-span-2 disabled:opacity-50"
          >
            {submitting ? 'Creating...' : 'Create Session'}
          </button>
        </form>
      </div>

      {/* Session List */}
      <h2 className="text-lg font-semibold mb-3">All Sessions</h2>
      <div className="space-y-2">
        {sessions.length === 0 && (
          <div className="text-gray-400 italic">No sessions yet.</div>
        )}
        {sessions.map(session => (
          <div
            key={session.id}
            onClick={() => handleSelect(session)}
            className={`flex items-center justify-between border rounded px-4 py-3 cursor-pointer transition
              ${activeSession?.id === session.id
                ? 'bg-blue-50 border-blue-400'
                : 'bg-white hover:bg-gray-50'
              }`}
          >
            <div>
              <span className="font-semibold">{session.name}</span>
              <span className="text-gray-500 text-sm ml-2">{session.date}</span>
            </div>
            <div className="text-sm text-gray-500">
              {session.start_time} → {session.end_time}
              {activeSession?.id === session.id && (
                <span className="ml-2 text-blue-600 font-semibold">● Active</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SessionManagement;