import { useState, useEffect } from 'react';
import api from '../api';

function LiveAttendance() {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAttendance = () => {
      api.get('/attendance/today/')
        .then(response => {
          setRecords(response.data.records);
          setError(null);
        })
        .catch(err => {
          setError('Could not reach backend');
        });
    };

    fetchAttendance(); // run once immediately
    const interval = setInterval(fetchAttendance, 3000); // then every 3 seconds

    return () => clearInterval(interval); // cleanup when leaving the page
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">Live Attendance</h1>
      <p className="text-gray-600 mb-4">
        Run <code className="bg-gray-200 px-1 rounded">recognize.py</code> to mark attendance —
        this page updates automatically.
      </p>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      <div className="space-y-2">
        {records.length === 0 && (
          <div className="text-gray-400 italic">No attendance marked yet today.</div>
        )}
        {records.map(record => (
          <div
            key={record.id}
            className="flex items-center justify-between bg-green-50 border border-green-200 rounded px-4 py-3"
          >
            <div>
              <span className="font-semibold">{record.student_name}</span>
              <span className="text-gray-500 ml-2">({record.student_roll})</span>
            </div>
            <span className="text-sm text-gray-500">
              {new Date(record.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LiveAttendance;