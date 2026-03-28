import { useNavigate } from 'react-router-dom'

export default function Membership() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-green-700 text-xl">←</button>
        <h2 className="text-lg font-bold flex-1 text-center">Membership</h2>
      </div>

      <div className="px-5 py-6">

        {/* Current Plan */}
        <h3 className="font-bold text-base mb-3">Your Current Plan</h3>
        <div className="bg-white border-2 border-green-700 rounded-2xl p-5 mb-6 text-center">
          <span className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">Current Plan</span>
          <p className="text-xl font-bold mt-3">Starter</p>
          <p className="text-gray-500 text-sm mt-1">500 AI replies per month</p>
        </div>

        {/* Other Plans */}
        <h3 className="font-bold text-base mb-3">Explore Other Plans</h3>

        {/* Free Trial */}
        <div className="bg-white rounded-2xl p-5 mb-4 text-center shadow-sm">
          <p className="text-lg font-bold">Free trial</p>
          <p className="text-gray-500 text-sm mt-1">PKR 0 / USD $0</p>
          <p className="text-gray-500 text-sm">100 lifetime replies</p>
        </div>

        {/* Growth */}
        <div className="bg-white rounded-2xl p-5 text-center shadow-sm">
          <p className="text-lg font-bold">Growth</p>
          <p className="text-gray-500 text-sm mt-1">PKR 3,499 / USD ~$12.50</p>
          <p className="text-gray-500 text-sm mb-4">Unlimited replies</p>
          <button
             onClick={() => navigate('/upgrade')} 
            className="w-full border-2 border-green-700 text-green-700 rounded-full py-3 font-semibold text-sm bg-white">  
                Upgrade
            </button>
        </div>

      </div>
    </div>
  )
}