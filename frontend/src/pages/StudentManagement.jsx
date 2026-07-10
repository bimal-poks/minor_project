import { useState, useEffect } from 'react';
import api from '../api';

function StudentManagement() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [rollNumber, setRollNumber] = useState('');
  const [name, setName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState(null);

  const fetchStudents = () => {
    setLoading(true);
    api.get('/students/')
      .then(response => {
        setStudents(response.data);
        setLoading(false);
      })
      .catch(err => {
        setError('Failed to load students. Is the backend running?');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormError(null);

    if (!rollNumber.trim() || !name.trim()) {
      setFormError('Both fields are required.');
      return;
    }

    setSubmitting(true);
    api.post('/students/', { roll_number: rollNumber.trim(), name: name.trim() })
      .then(() => {
        setRollNumber('');
        setName('');
        setSubmitting(false);
        fetchStudents(); // refresh the table
      })
      .catch(err => {
        const message = err.response?.data?.roll_number?.[0] || 'Failed to add student.';
        setFormError(message);
        setSubmitting(false);
      });
  };

  if (loading) return <div className="p-6">Loading students...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Student Management</h1>

      <form onSubmit={handleSubmit} className="bg-white border rounded-lg p-4 mb-6 flex gap-3 items-start">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Roll Number (e.g. 080BEI022)"
            value={rollNumber}
            onChange={(e) => setRollNumber(e.target.value)}
            className="border rounded px-3 py-2 w-full"
          />
        </div>
        <div className="flex-1">
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border rounded px-3 py-2 w-full"
          />
        </div>
        <button
          type="submit"
          disabled={submitting}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {submitting ? 'Adding...' : 'Add Student'}
        </button>
      </form>

      {formError && <div className="text-red-600 mb-4">{formError}</div>}

      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 px-4 py-2 text-left">Roll Number</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Name</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Added</th>
          </tr>
        </thead>
        <tbody>
          {students.map(student => (
            <tr key={student.id}>
              <td className="border border-gray-300 px-4 py-2">{student.roll_number}</td>
              <td className="border border-gray-300 px-4 py-2">{student.name}</td>
              <td className="border border-gray-300 px-4 py-2">
                {new Date(student.created_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StudentManagement;