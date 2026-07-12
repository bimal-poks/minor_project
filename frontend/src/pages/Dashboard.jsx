import { useState, useEffect } from 'react';
import api from '../api';

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [studentCount, setStudentCount] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get('/attendance/today/'),
      api.get('/students/')
    ])
      .then(([attendanceRes, studentsRes]) => {
        setSummary(attendanceRes.data);
        setStudentCount(studentsRes.data.length);
      })
      .catch((err) => {
        console.error(err);
        setError('Could not reach backend');
      });
  }, []);

  if (error) {
    return <div className="p-6 text-red-600">{error}</div>;
  }

  if (!summary) {
    return <div className="p-6">Loading dashboard...</div>;
  }

  const presentCount = summary.count;
  const attendanceRate =
    studentCount > 0
      ? ((presentCount / studentCount) * 100).toFixed(1)
      : 0;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>

        <a
          href={`http://127.0.0.1:8000/api/attendance/export/?date=${summary?.date || ''}`}
          className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700"
          download
        >
          Download CSV
        </a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white border rounded-lg p-6 shadow-sm">
          <div className="text-gray-500 text-sm mb-1">
            Total Students
          </div>
          <div className="text-3xl font-bold">
            {studentCount}
          </div>
        </div>

        <div className="bg-white border rounded-lg p-6 shadow-sm">
          <div className="text-gray-500 text-sm mb-1">
            Present Today
          </div>
          <div className="text-3xl font-bold text-green-600">
            {presentCount}
          </div>
        </div>

        <div className="bg-white border rounded-lg p-6 shadow-sm">
          <div className="text-gray-500 text-sm mb-1">
            Attendance Rate
          </div>
          <div className="text-3xl font-bold text-blue-600">
            {attendanceRate}%
          </div>
        </div>
      </div>

      <h2 className="text-lg font-semibold mb-3">
        Today's Records ({summary.date})
      </h2>

      <div className="space-y-2">
        {summary.records.length === 0 && (
          <div className="text-gray-400 italic">
            No attendance marked yet today.
          </div>
        )}

        {summary.records.map((record) => (
          <div
            key={record.id}
            className="flex items-center justify-between bg-white border rounded px-4 py-3"
          >
            <div>
              <span className="font-semibold">
                {record.student_name}
              </span>
              <span className="text-gray-500 ml-2">
                ({record.student_roll})
              </span>
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

export default Dashboard;