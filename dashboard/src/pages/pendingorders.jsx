import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'

export default function PendingOrders() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPendingOrders()
  }, [])

  const fetchPendingOrders = async () => {
    const { data, error } = await supabase
      .from('orders')
      .select('*')
      .eq('status', 'new')
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error:', error)
    } else {
      setOrders(data)
    }
    setLoading(false)
  }

  const markCompleted = async (id) => {
    const { error } = await supabase
      .from('orders')
      .update({ status: 'completed' })
      .eq('id', id)

    if (!error) {
      setOrders(orders.filter(o => o.id !== id))
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-xl">←</button>
        <h2 className="text-lg font-bold">Pending Orders</h2>
      </div>

      <div className="px-5 py-4 flex flex-col gap-4">
        {loading ? (
          <p className="text-center text-gray-400 py-6">Loading...</p>
        ) : orders.length === 0 ? (
          <p className="text-center text-gray-400 py-6">No pending orders</p>
        ) : (
          orders.map(order => (
            <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <p className="font-bold">{order.customer_name}</p>
                <span className="text-xs border border-yellow-400 text-yellow-500 px-3 py-1 rounded-full">
                  Pending
                </span>
              </div>
              <p className="text-gray-500 text-sm mb-1">{order.product}</p>
              <p className="text-gray-500 text-sm mb-1">{order.phone_number}</p>
              <p className="text-gray-500 text-sm mb-4">{order.address}</p>
              <button
                onClick={() => markCompleted(order.id)}
                className="w-full bg-green-700 text-white rounded-full py-3 font-semibold text-sm"
              >
                Mark Completed
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}