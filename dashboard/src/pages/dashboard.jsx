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

  const parseOrderDate = (value) => {
    if (!value) return null

    if (value instanceof Date) {
      return isNaN(value.getTime()) ? null : value
    }

    const str = String(value).trim()

    const simpleTimestampMatch = str.match(
      /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?$/
    )

    if (simpleTimestampMatch) {
      const [, year, month, day, hour, minute, second, fraction = '0'] =
        simpleTimestampMatch

      const milliseconds = Number(fraction.slice(0, 3).padEnd(3, '0'))

      return new Date(
        Date.UTC(
          Number(year),
          Number(month) - 1,
          Number(day),
          Number(hour),
          Number(minute),
          Number(second),
          milliseconds
        )
      )
    }

    const parsed = new Date(str)
    return isNaN(parsed.getTime()) ? null : parsed
  }

  const getMinutesDiff = (date) => {
    const parsedDate = parseOrderDate(date)
    if (!parsedDate) return null

    const diff = Math.floor((Date.now() - parsedDate.getTime()) / 1000 / 60)
    return diff < 0 ? 0 : diff
  }

  const timeAgo = (date) => {
    const diff = getMinutesDiff(date)

    if (diff === null) return ''
    if (diff < 1) return 'Just now'
    if (diff < 60) return `${diff}m ago`
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`
    return `${Math.floor(diff / 1440)}d ago`
  }

  const isWithin6Hours = (date) => {
    const diff = getMinutesDiff(date)
    if (diff === null) return false
    return diff <= 360
  }

  const badgeText = (status, createdAt) => {
    const normalizedStatus = String(status || '').toLowerCase()

    if (normalizedStatus === 'completed') return 'Completed'
    if (isWithin6Hours(createdAt)) return 'New'
    return 'Pending'
  }

  const badgeStyle = (status, createdAt) => {
    const normalizedStatus = String(status || '').toLowerCase()

    if (normalizedStatus === 'completed') {
      return 'bg-gray-300 text-gray-700'
    }

    if (isWithin6Hours(createdAt)) {
      return 'bg-green-700 text-white'
    }

    return 'bg-yellow-400 text-gray-900'
  }

  const todayOrders = orders.filter((o) => {
    const orderDate = parseOrderDate(o.created_at)
    if (!orderDate) return false

    const now = new Date()

    return (
      orderDate.getFullYear() === now.getFullYear() &&
      orderDate.getMonth() === now.getMonth() &&
      orderDate.getDate() === now.getDate()
    )
  })

  const pendingOrders = orders.filter(
    (o) => String(o.status || '').toLowerCase() !== 'completed'
  )

  const completedOrders = orders.filter(
    (o) => String(o.status || '').toLowerCase() === 'completed'
  )

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white px-5 py-4 flex items-center justify-between">
        <button onClick={() => setMenuOpen(true)} className="text-2xl">
          ☰
        </button>
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
                      ? `${order.product.slice(0, 30)}...`
                      : order.product || 'No product'}
                  </p>
                </div>

                <div className="flex flex-col items-end gap-1">
                  <span
                    className={`text-xs px-3 py-1 rounded-full font-medium ${badgeStyle(
                      order.status,
                      order.created_at
                    )}`}
                  >
                    {badgeText(order.status, order.created_at)}
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