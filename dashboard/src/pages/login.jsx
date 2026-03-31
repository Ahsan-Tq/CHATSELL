import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Please enter email and password')
      return
    }

    setLoading(true)
    setError('')

    const { error } = await supabase.auth.signInWithPassword({ email, password })

    if (error) {
      setError('Invalid email or password')
      setLoading(false)
    } else {
      navigate('/dashboard')
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-6">
      <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-sm">

        <h1 className="text-center text-3xl font-bold mb-8">
          <span className="text-black">Chat</span>
          <span className="text-green-700">Sell</span>
        </h1>

        {error && (
          <p className="text-red-500 text-sm text-center mb-4">{error}</p>
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full bg-gray-100 rounded-full px-5 py-4 mb-4 text-sm outline-none"
        />

        <div className="relative mb-6">
          <input
            type={showPassword ? 'text' : 'password'}
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full bg-gray-100 rounded-full px-5 py-4 text-sm outline-none"
          />
          <button
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-5 top-4 text-gray-400"
          >
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>

        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-green-700 text-white rounded-full py-4 font-semibold mb-4"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>

        <p className="text-center text-sm underline text-gray-600 mb-6 cursor-pointer">
          Forgot Password
        </p>

        <p className="text-center text-xs text-gray-400">
          Manage orders automatically
        </p>

      </div>
    </div>
  )
}