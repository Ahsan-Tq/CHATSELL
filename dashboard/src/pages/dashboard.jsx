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

    // Handles: 2026-04-08 16:39:02.21079
    const simpleTimestampMatch = str.match(
