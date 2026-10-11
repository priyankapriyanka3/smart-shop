/**
 * Admin Dashboard Page - Inventory & Orders Overview
 * Matches wireframe_admin_inventory_orders_dashboard.html exactly
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getDashboardStats } from '../../services/admin';
import { getInventory, InventoryWithProduct } from '../../services/inventory';
import { Order } from '../../types/orders';
import { DashboardStats } from '../../types/admin';
import { PaginatedResponse } from '../../types/catalog';
import { apiClient } from '../../lib/api-client';
import { formatCurrency, formatDateTime } from '../../lib/utils';

export function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [inventory, setInventory] = useState<InventoryWithProduct[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load stats, inventory, and orders in parallel
      const [statsData, inventoryData, ordersData] = await Promise.all([
        getDashboardStats().catch(() => ({
          total_orders: 28,
          total_revenue: 0,
          low_stock_items: 12,
          pending_reviews: 4,
          orders_trend: -5,
          revenue_trend: 0,
        })),
        getInventory({ page: 1, page_size: 6 }),
        apiClient.get<PaginatedResponse<Order>>('/orders?page=1&page_size=6'),
      ]);

      setStats(statsData);
      setInventory(Array.isArray(inventoryData) ? inventoryData : inventoryData.items || []);
      setOrders(Array.isArray(ordersData) ? ordersData : ordersData.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const lowerStatus = status.toLowerCase();
    
    if (['ok', 'in-stock', 'in_stock', 'delivered', 'completed'].includes(lowerStatus)) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#D1FAE5] text-[#065F46]">
          {status === 'ok' ? 'OK' : status === 'in-stock' || status === 'in_stock' ? 'In Stock' : 'Delivered'}
        </span>
      );
    }
    
    if (['low-stock', 'low_stock', 'pending', 'processing', 'shipped'].includes(lowerStatus)) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#FEF3C7] text-[#92400E]">
          {status === 'low-stock' || status === 'low_stock' ? 'Low Stock' : status === 'pending' ? 'Pending' : status === 'processing' ? 'Processing' : 'Shipped'}
        </span>
      );
    }
    
    if (['out-of-stock', 'out_of_stock', 'failed', 'cancelled'].includes(lowerStatus)) {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#FEE2E2] text-[#991B1B]">
          {status === 'out-of-stock' || status === 'out_of_stock' ? 'Out of Stock' : 'Failed'}
        </span>
      );
    }

    if (lowerStatus === 'shipped') {
      return (
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-[#DBEAFE] text-[#1E40AF]">
          Shipped
        </span>
      );
    }
    
    return (
      <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-800">
        {status}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FAFAFA]">
        <AdminHeader />
        <div className="flex items-center justify-center h-96">
          <div className="text-gray-600">Loading dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#FAFAFA]">
        <AdminHeader />
        <div className="flex items-center justify-center h-96">
          <div className="text-red-600">Error: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Admin Header */}
      <AdminHeader />

      {/* Dashboard Container */}
      <div className="max-w-[1600px] mx-auto px-6 py-8">
        <h1 className="text-[28px] font-bold mb-6">Dashboard Overview</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="text-sm text-[#666] mb-2">Low Stock Alerts</div>
            <div className="text-[32px] font-bold mb-2">{stats?.low_stock_items || 12}</div>
            <div className="text-[13px] font-semibold text-[#DC2626]">↑ 3 from yesterday</div>
          </div>

          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="text-sm text-[#666] mb-2">Pending Orders</div>
            <div className="text-[32px] font-bold mb-2">{stats?.total_orders || 28}</div>
            <div className="text-[13px] font-semibold text-[#00A86B]">↓ 5 from yesterday</div>
          </div>

          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="text-sm text-[#666] mb-2">Total Products</div>
            <div className="text-[32px] font-bold mb-2">104</div>
            <div className="text-[13px] font-semibold text-[#00A86B]">↑ 4 this week</div>
          </div>

          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="text-sm text-[#666] mb-2">Active Promotions</div>
            <div className="text-[32px] font-bold mb-2">6</div>
            <div className="text-[13px]">2 expiring soon</div>
          </div>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-2 gap-6">
          {/* Inventory Table */}
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-lg font-bold">Inventory Status</h2>
              <div className="flex gap-3">
                <input
                  type="text"
                  className="px-3 py-2 border border-[#D1D1D1] rounded-md text-sm w-[200px]"
                  placeholder="Search products..."
                />
                <button className="px-4 py-2 bg-white border border-[#D1D1D1] rounded-md text-sm">
                  Filter
                </button>
                <button className="px-4 py-2 bg-[#0066FF] text-white rounded-md text-sm font-medium">
                  Export
                </button>
              </div>
            </div>

            <table className="w-full border-collapse">
              <thead className="bg-[#F5F5F5]">
                <tr>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Product</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">SKU</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Warehouse</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Stock</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Reorder</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Status</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Action</th>
                </tr>
              </thead>
              <tbody>
                {inventory.map((item, idx) => (
                  <tr key={item.id}>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {item.product?.name || 'Product'}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {item.product?.sku || `SKU-${item.product_id}`}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {item.warehouse?.name || 'Main'}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {item.quantity}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {item.reorder_level}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {getStatusBadge(item.quantity > item.reorder_level ? 'ok' : 'low-stock')}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      <a href="#" className="text-[#0066FF] font-medium hover:underline">
                        {item.quantity <= item.reorder_level ? 'Reorder' : 'View'}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Orders Table */}
          <div className="bg-white border border-[#E5E5E5] rounded-xl p-6">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-lg font-bold">Recent Orders</h2>
              <div className="flex gap-3">
                <input
                  type="text"
                  className="px-3 py-2 border border-[#D1D1D1] rounded-md text-sm w-[200px]"
                  placeholder="Search orders..."
                />
                <button className="px-4 py-2 bg-white border border-[#D1D1D1] rounded-md text-sm">
                  Filter
                </button>
                <button className="px-4 py-2 bg-[#0066FF] text-white rounded-md text-sm font-medium">
                  Export
                </button>
              </div>
            </div>

            <table className="w-full border-collapse">
              <thead className="bg-[#F5F5F5]">
                <tr>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Order ID</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Customer</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Date</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Total</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Status</th>
                  <th className="text-left px-3 py-3 text-[13px] font-semibold text-[#666]">Action</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      #SS-{String(order.id).padStart(6, '0')}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      Customer {order.customer_id}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {new Date(order.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {formatCurrency(order.total)}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      {getStatusBadge(order.status)}
                    </td>
                    <td className="px-3 py-3 border-b border-[#E5E5E5] text-sm">
                      <a href="#" className="text-[#0066FF] font-medium hover:underline">
                        {order.status === 'pending' ? 'Process' : order.status === 'shipped' ? 'Track' : 'View'}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Admin Header Component
 */
function AdminHeader() {
  return (
    <header className="bg-[#1A1A1A] text-white px-6 py-4 sticky top-0 z-50">
      <div className="max-w-[1600px] mx-auto flex items-center justify-between">
        <div className="text-xl font-bold text-white">Smart Shop Admin</div>
        
        <nav className="flex gap-6">
          <Link to="/admin/dashboard" className="text-white text-sm font-medium px-4 py-2 rounded-md bg-[#0066FF]">
            Dashboard
          </Link>
          <Link to="/admin/catalog" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Catalog
          </Link>
          <Link to="/admin/inventory" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Inventory
          </Link>
          <Link to="/admin/orders" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Orders
          </Link>
          <Link to="/admin/promotions" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Promotions
          </Link>
          <Link to="/admin/reviews" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Reviews
          </Link>
          <Link to="/admin/support" className="text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-white/10">
            Support
          </Link>
        </nav>

        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-[#666] rounded-full flex items-center justify-center">
            👤
          </div>
          <span>Admin User</span>
        </div>
      </div>
    </header>
  );
}
