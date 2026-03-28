import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function EditProfile() {
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/account')} className="text-green-700 text-xl">←</button>
        <h2 className="text-lg font-bold flex-1 text-center">Edit Profile</h2>
      </div>

      <div className="px-5 py-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm">

          {/* Avatar */}
          <div className="flex flex-col items-center mb-6">
            <div className="relative">
              <div className="w-20 h-20 rounded-full bg-gray-300 flex items-center justify-center">
                <svg viewBox="0 0 24 24" className="w-12 h-12 text-gray-400" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
              </div>
              <div className="absolute bottom-0 right-0 bg-gray-200 rounded-full p-1">
                <svg viewBox="0 0 24 24" className="w-4 h-4 text-gray-600" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </div>
            </div>
            <button className="mt-2 border border-green-700 text-green-700 text-xs px-4 py-1 rounded-full">
              Change Photo
            </button>
          </div>

          {/* Fields */}
          {['Full Name', 'Email', 'Phone Number', 'Business Name', 'Business Phone Number'].map(field => (
            <input
              key={field}
              type="text"
              placeholder={field}
              className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm mb-3 outline-none"
            />
          ))}

          {/* Password */}
          <div className="relative mb-6">
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Password"
              defaultValue="password123"
              className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none"
            />
            <button
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-3 text-gray-400"
            >
              {showPassword ? '👁️' : '🙈'}
            </button>
          </div>

          <button className="w-full bg-green-700 text-white rounded-full py-4 font-semibold text-sm">
            Save Changes
          </button>

        </div>
      </div>

    </div>
  )
}