import { useNavigate } from 'react-router-dom'

export default function Menu({ onClose }) {
  const navigate = useNavigate()

  const go = (path) => {
    navigate(path)
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 flex">
      
      {/* Backdrop */}
      <div className="flex-1 bg-black opacity-30" onClick={onClose} />

      {/* Menu Panel */}
      <div className="absolute left-0 top-0 bottom-0 w-4/5 bg-white rounded-r-3xl p-6 flex flex-col">
        
        <h1 className="text-2xl font-bold mb-8">
          <span className="text-black">Chat</span>
          <span className="text-green-700">Sell</span>
        </h1>

        <div className="flex flex-col gap-3 flex-1">
          {[
            { label: 'Dashboard', icon: '⊞', path: '/dashboard' },
            { label: 'Pending Orders', icon: '🕐', path: '/pending' },
            { label: 'Completed Orders', icon: '✓', path: '/completed' },
            { label: 'Account', icon: '👤', path: '/account' },
            { label: 'Membership', icon: '🏅', path: '/membership' },
          ].map(item => (
            <button
              key={item.label}
              onClick={() => go(item.path)}
              className="flex items-center gap-4 border border-gray-200 rounded-2xl px-4 py-4 text-left text-sm font-medium"
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>

        <button
          onClick={() => go('/login')}
          className="flex items-center justify-center gap-2 border-2 border-green-700 rounded-2xl px-4 py-4 text-sm font-medium text-green-700 mt-4"
        >
          Logout →
        </button>

      </div>
    </div>
  )
}