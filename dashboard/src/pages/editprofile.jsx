import { useNavigate } from 'react-router-dom'

export default function EditProfile() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-white px-5 py-4 flex items-center gap-4 shadow-sm">
        <button onClick={() => navigate('/account')} className="text-green-700 text-xl font-bold">←</button>
        <h2 className="text-lg font-bold flex-1 text-center pr-6">Edit Profile</h2>
      </div>

      {/* Message Card Container */}
      <div className="px-5 py-10">
        <div className="bg-white rounded-2xl p-8 shadow-sm text-center">
          
          <h3 className="text-lg font-bold text-gray-900 mb-4">
            Update your profile
          </h3>
          
          <p className="text-gray-600 text-sm mb-4">
            To update your profile details, contact our support team.
          </p>
          
          <p className="font-bold text-gray-900 text-sm mb-4">
            support@chatsell.com
          </p>
          
          <p className="text-gray-500 text-sm">
            Our team will help you update your information quickly.
          </p>

        </div>
      </div>

    </div>
  )
}