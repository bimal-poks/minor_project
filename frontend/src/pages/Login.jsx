import { useState } from 'react';
import api from '../api';

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    api.post('/auth/login/', { username, password })
      .then(response => {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        setLoading(false);
        onLoginSuccess(response.data.username);
      })
      .catch(err => {
        setError('Invalid username or password');
        setLoading(false);
      });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white border rounded-lg p-8 shadow-sm w-80">
        <h1 className="text-xl font-bold mb-1">Smart Attendance System</h1>
        <p className="text-gray-500 text-sm mb-6">Sign in to continue</p>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border rounded px-3 py-2 w-full mb-3"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border rounded px-3 py-2 w-full mb-4"
        />

        {error && <div className="text-red-600 text-sm mb-3">{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white w-full py-2 rounded disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
    </div>
  );
}

export default Login;