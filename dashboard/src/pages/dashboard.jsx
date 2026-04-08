import { useState, useEffect } from 'react'
import { supabase } from '../supabase'
import Menu from '../components/menu'

export default function Dashboard() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    setLoading(true)

    const { data, error } = await supabase
      .from('orders')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching orders:', error)
    } else {
      setOrders(data || [])
    }

    setLoading(false)
  }

  const parseOrderDate = (dateString) => {
    if (!dateString) return null

    const normalized = dateString.includes('T')
      ? dateString
      : dateString.replace(' ', 'T')

    const hasTimezone = /([zZ]|[+-]\d{2}:\d{2})$$/.test(normalized)
    const finalDateString = hasTimezone ? normalized : `$${normalized}Z`

    const parsed = new Date(finalDateString)

    return isNaN(parsed.getTime()) ? null : parsed
  }

  const getMinutesDiff = (dateString) => {
    const orderDate = parseOrderDate(dateString)
    if (!orderDate) return null

    const diff = Math.floor((Date.now() - orderDate.getTime()) / 1000 / 60)
    return diff < 0 ? 0 : diff
  }

  const timeAgo = (dateString) => {
    const diff = getMinutesDiff(dateString)

    if (diff === null) return 'Invalid time'
    if (diff < 1) return 'Just now'
    if (diff < 60) return `$${diff}m ago`
    if (diff < 1440) return `$${Math.floor(diff / 60)}h ago`
    return `$${Math.floor(diff / 1440)}d ago`
  }

  const getAgeLabel = (dateString) => {
    const diff = getMinutesDiff(dateString)
    if (diff === null) return 'Old'
    return diff <= 720 ? 'New' : 'Old'
  }

  const getAgeBadgeStyle = (dateString) => {
    return getAgeLabel(dateString) === 'New'
      ? 'bg-green-700 text-white'
      : 'bg-gray-300 text-gray-700'
  }

  const getCompletionLabel = (status) => {
    return (status || '').toLowerCase() === 'completed' ? 'Completed' : 'Pending'
  }

  const getCompletionBadgeStyle = (status) => {
    return (status || '').toLowerCase() === 'completed'
      ? 'bg-blue-700 text-white'
      : 'bg-yellow-500 text-white'
  }

  const todayOrders = orders.filter((order) => {
    const orderDate = parseOrderDate(order.created_at)
    if (!orderDate) return false

    const now = new Date()

    return (
      orderDate.getFullYear() === now.getFullYear() &&
      orderDate.getMonth() === now.getMonth() &&
      orderDate.getDate() === now.getDate()
    )
  })

  const pendingOrders = orders.filter(
    (order) => (order.status || '').toLowerCase() !== 'completed'
  )

  const completedOrders = orders.filter(
    (order) => (order.status || '').toLowerCase() === 'completed'
  )

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white px-5 py-4 flex items-center justify-between">
        <button onClick={() => setMenuOpen(true)} className="text-2xl">☰</button>
        <h1 className="text-2xl font-bold">
          <span className="text-black">Chat</span>
          <span className="text-green-700">Sell</span>
        </h1>
        <div className="w-6" />
      </div>

      {menuOpen && <Menu onClose={() => setMenuOpen(false)} />}

      <div className="px-5 py-4">
        <div className="flex gap-3 mb-3">
          <div className="flex-1 bg-white rounded-2xl p-4 shadow-sm">
            <p className="text-gray-500 text-sm">Total Orders Today</p>
            <p className="text-4xl font-bold mt-1">{todayOrders.length}</p>
          </div>

          <div className="flex-1 bg-white rounded-2xl p-4 shadow-sm border-2 border-green-700">
            <p className="text-gray-500 text-sm">Pending Orders</p>
            <p className="text-4xl font-bold mt-1">{pendingOrders.length}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-4 shadow-sm mb-5">
          <p className="text-gray-500 text-sm">Completed Orders</p>
          <p className="text-4xl font-bold mt-1">{completedOrders.length}</p>
        </div>

        <h2 className="text-lg font-bold mb-3">Recent Orders list</h2>

        {loading ? (
          <p className="text-center text-gray-400 py-6">Loading orders...</p>
        ) : orders.length === 0 ? (
          <p className="text-center text-gray-400 py-6">No orders yet</p>
        ) : (
          <div className="flex flex-col gap-3">
            {orders.slice(0, 10).map((order) => (
              <div
                key={order.id}
                className="bg-white rounded-2xl p-4 shadow-sm flex items-start justify-between"
              >
                <div>
                  <p className="font-bold text-sm">
                    {order.customer_name || 'Unknown Customer'}
                  </p>
                  <p className="text-gray-500 text-sm mt-1">
                    {(order.product || '').length > 30
                      ? `$${order.product.slice(0, 30)}...`
                      : order.product || 'No product'}
                  </p>
                </div>

                <div className="flex flex-col items-end gap-1">
                  <span
                    className={`text-xs px-3 py-1 rounded-full font-medium $${getAgeBadgeStyle(order.created_at)}`}
                  >
                    {getAgeLabel(order.created_at)}
                  </span>

                  <span
                    className={`text-xs px-3 py-1 rounded-full font-medium $${getCompletionBadgeStyle(order.status)}`}
                  >
                    {getCompletionLabel(order.status)}
                  </span>

                  <span className="text-xs text-gray-400">
                    {timeAgo(order.created_at)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
