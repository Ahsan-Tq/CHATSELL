import { useNavigate } from 'react-router-dom'

export default function PendingOrders() {
  const navigate = useNavigate()

  // Placeholder data — we'll connect real data tomorrow
  const orders = [
    { id: 1, name: 'Ahmed Khan', product: 'Black Hoodie Large', phone: '923001234567', address: 'House 5 Block B DHA Lahore' },
    { id: 2, name: 'Sara Ali', product: 'Embroidered Shirt Medium', phone: '923009876543', address: 'Flat 3 Gulberg III Lahore' },
    { id: 3, name: 'Usman Malik', product: 'Nihari 2 portions', phone: '923331234567', address: 'Street 7 F-10 Islamabad' },
  ]

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-xl">←</button>
        <h2 className="text-lg font-bold">Pending Orders</h2>
      </div>

      <div className="px-5 py-4 flex flex-col gap-4">
        {orders.map(order => (
          <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm">
            
            <div className="flex items-center justify-between mb-2">
              <p className="font-bold">{order.name}</p>
              <span className="text-xs border border-yellow-400 text-yellow-500 px-3 py-1 rounded-full">
                Pending
              </span>
            </div>

            <p className="text-gray-500 text-sm mb-1">
              {order.product.length > 35 ? order.product.slice(0, 35) + '...' : order.product}
            </p>
            <p className="text-gray-500 text-sm mb-1">{order.phone}</p>
            <p className="text-gray-500 text-sm mb-4">
              {order.address.length > 40 ? order.address.slice(0, 40) + '...' : order.address}
            </p>

            <button className="w-full bg-green-700 text-white rounded-full py-3 font-semibold text-sm">
              Mark Completed
            </button>

          </div>
        ))}
      </div>

    </div>
  )
}