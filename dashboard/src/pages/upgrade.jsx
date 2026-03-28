import { useNavigate } from 'react-router-dom'

export default function Upgrade() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/membership')} className="text-green-700 text-xl">←</button>
        <h2 className="text-lg font-bold flex-1 text-center">Upgrade Plan</h2>
      </div>

      <div className="px-5 py-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm text-center">
          <p className="text-xl font-bold mb-3">Upgrade your plan</p>
          <p className="text-gray-500 text-sm mb-4">
            To upgrade your Chatsell membership, contact our support team.
          </p>
          <p className="font-bold text-sm mb-4">support@chatsell.com</p>
          <p className="text-gray-500 text-sm mb-6">
            Our team will help you activate your new plan quickly.
          </p>
          <button className="w-full bg-green-700 text-white rounded-full py-4 font-semibold text-sm">
            Contact Support
          </button>
        </div>
      </div>

    </div>
  )
}