import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'

export default function Membership() {
  const navigate = useNavigate()
  const [membership, setMembership] = useState('Free Trial')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMembership()
  }, [])

  const fetchMembership = async () => {
    const { data: { session } } = await supabase.auth.getSession()
    if (!session) return

    const { data, error } = await supabase
      .from('sellers')
      .select('membership')
      .eq('id', session.user.id)
      .single()

    if (!error && data) setMembership(data.membership || 'Free Trial')
    setLoading(false)
  }

  const plans = [
    { name: 'Free Trial', price: 'PKR 0 / USD $0', description: '100 lifetime replies' },
    { name: 'Starter', price: 'PKR 1,999 / USD ~$7', description: '500 AI replies per month' },
    { name: 'Growth', price: 'PKR 3,499 / USD ~$12.50', description: 'Unlimited replies' },
  ]

  const currentPlan = plans.find(p => p.name === membership) || plans[0]
  const otherPlans = plans.filter(p => p.name !== membership)

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-gray-400">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-green-700 text-xl">←</button>
        <h2 className="text-lg font-bold flex-1 text-center">Membership</h2>
      </div>

      <div className="px-5 py-6">

        <h3 className="font-bold text-base mb-3">Your Current Plan</h3>
        <div className="bg-white border-2 border-green-700 rounded-2xl p-5 mb-6 text-center">
          <span className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">Current Plan</span>
          <p className="text-xl font-bold mt-3">{currentPlan.name}</p>
          <p className="text-gray-500 text-sm mt-1">{currentPlan.description}</p>
          <p className="text-gray-400 text-xs mt-1">{currentPlan.price}</p>
        </div>

        <h3 className="font-bold text-base mb-3">Explore Other Plans</h3>

        <div className="flex flex-col gap-4">
          {otherPlans.map(plan => (
            <div key={plan.name} className="bg-white rounded-2xl p-5 text-center shadow-sm">
              <p className="text-lg font-bold">{plan.name}</p>
              <p className="text-gray-500 text-sm mt-1">{plan.price}</p>
              <p className="text-gray-500 text-sm mb-4">{plan.description}</p>
              {plan.name === 'Growth' && (
                <button
                  onClick={() => navigate('/upgrade')}
                  className="w-full border-2 border-green-700 text-green-700 rounded-full py-3 font-semibold text-sm bg-white"
                >
                  Upgrade
                </button>
              )}
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}