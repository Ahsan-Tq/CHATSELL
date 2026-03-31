import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'

export default function Account() {
  const navigate = useNavigate()
  const [seller, setSeller] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSeller()
  }, [])

  const fetchSeller = async () => {
    const { data: { session } } = await supabase.auth.getSession()

    if (!session) return

    const { data, error } = await supabase
      .from('sellers')
      .select('*')
      .eq('id', session.user.id)
      .single()

    if (!error) setSeller(data)
    setLoading(false)
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-400">Loading...</p>
      </div>
    )
  }

  const fields = [
    { label: 'Full Name', value: seller?.full_name },
    { label: 'Email', value: seller?.email },
    { label: 'Phone Number', value: seller?.phone_number },
    { label: 'Business Name', value: seller?.business_name },
    { label: 'Business Phone', value: seller?.business_phone },
    { label: 'Membership', value: seller?.membership || 'Free Trial' },
  ]

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-green-700 text-xl">←</button>
        <h2 className="text-lg font-bold flex-1 text-center">Account</h2>
      </div>

      <div className="px-5 py-6">
        <div className="bg-white rounded-2xl overflow-hidden shadow-sm mb-6">

          <div className="flex justify-center pt-6 pb-4">
            <div className="w-20 h-20 rounded-full bg-gray-300 flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="w-12 h-12 text-gray-400" fill="currentColor">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
              </svg>
            </div>
          </div>

          {fields.map((field, i) => (
            <div
              key={field.label}
              className={`px-6 py-4 flex justify-between items-center text-sm ${i < fields.length - 1 ? 'border-b border-gray-100' : ''}`}
            >
              <span className="text-gray-400">{field.label}</span>
              <span className="font-medium text-gray-800">{field.value || '—'}</span>
            </div>
          ))}
        </div>

        <button
          onClick={() => navigate('/editprofile')}
          className="w-full border-2 border-green-700 text-green-700 rounded-full py-4 font-semibold text-sm bg-white mb-3"
        >
          Edit Profile
        </button>

        <button
          onClick={handleLogout}
          className="w-full border-2 border-red-400 text-red-400 rounded-full py-4 font-semibold text-sm bg-white"
        >
          Logout
        </button>

      </div>
    </div>
  )
}