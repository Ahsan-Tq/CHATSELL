import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Menu from '../components/menu'

export default function Dashboard() {
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  // Placeholder stats — we'll connect real data tomorrow
  const stats = {
    totalToday: 12,
    pending: 5,
    completed: 7
  }

  const recentOrders = [
    { id: 1, name: 'Ahmed Khan', product: 'Black Hoodie Large', status: 'new', time: '10m ago' },
    { id: 2, name: 'Sara Ali', product: 'Embroidered Shirt Medium', status: 'pending', time: '2h ago' },
    { id: 3, name: 'Usman Malik', product: 'Nihari 2 portions', status: 'completed', time: '2h ago' },
    { id: 4, name: 'Fatima Zahra', product: 'Handmade jewelry set', status: 'completed', time: '3h ago' },
  ]

  const badgeStyle = (status) => {
    if (status === 'new') return 'bg-green-700 text-white'
    if (status === 'pending') return 'bg-yellow-400 text-white'
    return 'bg-gray-300 text-gray-700'
  }

  return (
    <div className="min-h-screen bg-gray-100">
      
      {/* Header */}
      <div className="bg-white px-5 py-4 flex items-center justify-between">
        <button onClick={() => setMenuOpen(true)} className="text-2xl">☰</button>
        <h1 className="text-2xl font-bold">
          <span className="text-black">Chat</span>
          <span className="text-green-700">Sell</span>
        </h1>
        <div className="w-6" />
      </div>

      {/* Menu */}
      {menuOpen && <Menu onClose={() => setMenuOpen(false)} />}

      <div className="px-5 py-4">

        {/* Stats */}
        <div className="flex gap-3 mb-3">
          <div className="flex-1 bg-white rounded-2xl p-4 shadow-sm">
            <p className="text-gray-500 text-sm">Total Orders Today</p>
            <p className="text-4xl font-bold mt-1">{stats.totalToday}</p>
          </div>
          <div className="flex-1 bg-white rounded-2xl p-4 shadow-sm border-2 border-green-700">
            <p className="text-gray-500 text-sm">Pending Orders</p>
            <p className="text-4xl font-bold mt-1">{stats.pending}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm mb-5">
          <p className="text-gray-500 text-sm">Completed Orders</p>
          <p className="text-4xl font-bold mt-1">{stats.completed}</p>
        </div>

        {/* Recent Orders */}
        <h2 className="text-lg font-bold mb-3">Recent Orders list</h2>

        <div className="flex flex-col gap-3">
          {recentOrders.map(order => (
            <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm flex items-start justify-between">
              <div>
                <p className="font-bold text-sm">{order.name}</p>
                <p className="text-gray-500 text-sm mt-1">
                  {order.product.length > 30 ? order.product.slice(0, 30) + '...' : order.product}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs px-3 py-1 rounded-full font-medium ${badgeStyle(order.status)}`}>
                  {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                </span>
                <span className="text-xs text-gray-400">{order.time}</span>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}