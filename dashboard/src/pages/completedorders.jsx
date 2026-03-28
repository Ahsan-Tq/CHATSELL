import { useNavigate } from 'react-router-dom'

export default function CompletedOrders() {
  const navigate = useNavigate()

  const orders = [
    { id: 1, name: 'Jane Cooper', product: 'A modern lamp and desk combo', date: 'Oct 27, 2023' },
    { id: 2, name: 'Ahmed Khan', product: 'Black Hoodie Large', date: 'Oct 27, 2023' },
    { id: 3, name: 'Sara Ali', product: 'Embroidered Shirt Medium', date: 'Oct 17, 2023' },
    { id: 4, name: 'Usman Malik', product: 'Nihari 2 portions', date: 'Oct 17, 2023' },
  ]

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-white px-5 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/dashboard')} className="text-xl">←</button>
        <h2 className="text-lg font-bold">Completed Orders</h2>
      </div>

      <div className="px-5 py-4 flex flex-col gap-4">
        {orders.map(order => (
          <div key={order.id} className="bg-white rounded-2xl p-4 shadow-sm">

            <div className="flex items-center justify-between mb-2">
              <p className="font-bold">{order.name}</p>
              <span className="text-xs border border-green-700 text-green-700 px-3 py-1 rounded-full">
                Completed
              </span>
            </div>

            <p className="text-gray-500 text-sm mb-1">
              {order.product.length > 35 ? order.product.slice(0, 35) + '...' : order.product}
            </p>
            <p className="text-gray-400 text-sm">Completed {order.date}</p>

          </div>
        ))}
      </div>

    </div>
  )
}
