import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabase'

export default function CompletedOrders() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCompletedOrders()
  }, [])

  const fetchCompletedOrders = async () => {
    const { data, error } = await supabase
      .from('orders')
      .select('*')
      .eq('status', 'completed')
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error:', error)
    } else {
      setOrders(data)
    }
    setLoading(false)
  }

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric'
    })
  }

  return (
    <div className="min-h-screen bg-gray-100">

      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-xl">←</button>
        <h2 className="text-lg font-bold">Completed Orders</h2>
      </div>

      <div className="px-5 py-4 flex flex-col gap-4">
        {loading ? (
          <p className="text-center text-gray-400 py-6">Loading...</p>
        ) : orders.length === 0 ? (
          <p className="text-center text-gray-400 py-6">No completed orders yet</p>
        ) : (
          orders.map(order => (
            <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <p className="font-bold">{order.customer_name}</p>
                <span className="text-xs border border-green-700 text-green-700 px-3 py-1 rounded-full">
                  Completed
                </span>
              </div>
              <p className="text-gray-500 text-sm mb-1">{order.product}</p>
              <p className="text-gray-400 text-sm">Completed {formatDate(order.created_at)}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}