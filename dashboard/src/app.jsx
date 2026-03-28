import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/login'
import Dashboard from './pages/dashboard'
import PendingOrders from './pages/pendingorders'
import CompletedOrders from './pages/completedorders'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/pending" element={<PendingOrders />} />
        <Route path="/completed" element={<CompletedOrders />} />
      </Routes>
    </BrowserRouter>
  )
}