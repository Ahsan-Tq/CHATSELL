import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/login'
import Dashboard from './pages/dashboard'
import PendingOrders from './pages/pendingorders'
import CompletedOrders from './pages/completedorders'
import Account from './pages/account'
import Membership from './pages/membership'
import Upgrade from './pages/upgrade'
import EditProfile from './pages/editprofile'
import ProtectedRoute from './components/protectedroute'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/pending" element={<ProtectedRoute><PendingOrders /></ProtectedRoute>} />
        <Route path="/completed" element={<ProtectedRoute><CompletedOrders /></ProtectedRoute>} />
        <Route path="/account" element={<ProtectedRoute><Account /></ProtectedRoute>} />
        <Route path="/membership" element={<ProtectedRoute><Membership /></ProtectedRoute>} />
        <Route path="/upgrade" element={<ProtectedRoute><Upgrade /></ProtectedRoute>} />
        <Route path="/editprofile" element={<ProtectedRoute><EditProfile /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}