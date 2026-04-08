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
      setOrders([])
    } else {
      setOrders(data || [])
    }

    setLoading(false)
  }

  const parseOrderDate = (value) => {
    if (!value) return null

    let str = String(value).trim()

    // convert "2026-04-08 16:39:02.21079" to ISO-like format
    str = str.replace(' ', 'T')

    // trim microseconds to milliseconds because JS Date can fail on long fractions
    str = str.replace(/\.(\d{3})\d+/, '.$$1')

    // if no timezone is present, treat it as UTC
    if (!/(Z|[+-]\d{2}:\d{2})$$/i.test(str)) {
      str += 'Z'
    }

    const date = new Date(str)
    return isNaN(date.getTime()) ? null : date
  }

  const getMinutesDiff = (createdAt) => {
    const orderDate = parseOrderDate(createdAt)
    if (!orderDate) return null

    const diff = Math.floor((Date.now() - orderDate.getTime()) / 60000)
    return diff < 0 ? 0 : diff
  }

  const timeAgo = (createdAt) => {
    const diff = getMinutesDiff(createdAt)

    if (diff === null) return 'Time error'
    if (diff < 1) return 'Just now'
    if (diff < 60) return `$${diff}m ago`
    if (diff < 1440) return `$${Math.floor(diff / 60)}h ago`
    return `$${Math.floor(diff / 1440)}d ago`
  }

  const getAgeLabel = (createdAt) => {
    const diff = getMinutesDiff(createdAt)
    if (diff === null) return 'Old'
    return diff <= 720 ? 'New' : 'Old'
  }

  const getAgeBadgeClass = (createdAt) => {
    return getAgeLabel(createdAt) === 'New'
      ? 'bg-green-700 text-white'
      : 'bg-gray-300 text-gray-700'
  }

  const getCompletionLabel = (status) => {
    return String(status || '').toLowerCase() === 'completed'
      ? 'Completed'
      : 'Pending'
  }

  const getCompletionBadgeClass = (status) => {
    return String(status || '').toLowerCase() === 'completed'
      ? 'bg-blue-700 text-white'
      : 'bg-yellow-400 text-black'
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
    (order) => String(order.status || '').toLowerCase() !== 'completed'
  )

  const completedOrders = orders.filter(
    (order) => String(order.status || '').toLowerCase() === 'completed'
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
                    {order.product && order.product.length > 30
                      ? `$${order.product.slice(0, 30)}...`
                      : order.product || 'No product'}
                  </p>
                </div>

                <div className="flex flex-col items-end gap-2">
                  <div className="flex gap-2 flex-wrap justify-end">
                    <span className={`text-xs px-3 py-1 rounded-full font-medium $${getAgeBadgeClass(order.created_at)}`}>
                      {getAgeLabel(order.created_at)}
                    </span>

                    <span className={`text-xs px-3 py-1 rounded-full font-medium $${getCompletionBadgeClass(order.status)}`}>
                      {getCompletionLabel(order.status)}
                    </span>
                  </div>

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
