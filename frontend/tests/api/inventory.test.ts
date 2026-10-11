/**
 * Tests for inventory API
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { inventoryApi } from '../../src/api/inventory';
import { apiClient } from '../../src/api/client';
import type { Inventory, InventoryUpdate, LowStockItem } from '../../src/types/inventory';
import type { PaginatedResponse } from '../../src/types/common';

vi.mock('../../src/api/client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('inventoryApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getInventory', () => {
    it('should call GET /inventory with no params', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [
          {
            id: 1,
            product_id: 1,
            product_name: 'Test Product',
            product_sku: 'TEST-001',
            warehouse_id: 1,
            warehouse_name: 'Main Warehouse',
            quantity: 100,
            reorder_level: 10,
            last_updated: '2024-01-01T00:00:00Z',
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-01-01T00:00:00Z',
          },
        ],
        total: 1,
        page: 1,
        per_page: 20,
        pages: 1,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.getInventory();

      expect(apiClient.get).toHaveBeenCalledWith('/inventory');
      expect(result).toEqual(mockResponse);
    });

    it('should call GET /inventory with pagination params', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [],
        total: 50,
        page: 2,
        per_page: 10,
        pages: 5,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await inventoryApi.getInventory({ page: 2, per_page: 10 });

      expect(apiClient.get).toHaveBeenCalledWith('/inventory?page=2&per_page=10');
    });

    it('should handle empty inventory', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [],
        total: 0,
        page: 1,
        per_page: 20,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.getInventory();

      expect(result.items).toHaveLength(0);
      expect(result.total).toBe(0);
    });

    it('should return inventory with product and warehouse details', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [
          {
            id: 1,
            product_id: 1,
            product_name: 'iPhone 15',
            product_sku: 'APL-001',
            warehouse_id: 1,
            warehouse_name: 'US-EAST-WH1',
            quantity: 250,
            reorder_level: 50,
            last_updated: '2024-07-01T00:00:00Z',
            created_at: '2024-01-01T00:00:00Z',
            updated_at: '2024-07-01T00:00:00Z',
          },
        ],
        total: 1,
        page: 1,
        per_page: 20,
        pages: 1,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.getInventory();

      expect(result.items[0].product_name).toBe('iPhone 15');
      expect(result.items[0].warehouse_name).toBe('US-EAST-WH1');
      expect(result.items[0].quantity).toBe(250);
    });

    it('should handle page param only', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [],
        total: 0,
        page: 3,
        per_page: 20,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await inventoryApi.getInventory({ page: 3 });

      expect(apiClient.get).toHaveBeenCalledWith('/inventory?page=3');
    });

    it('should handle per_page param only', async () => {
      const mockResponse: PaginatedResponse<Inventory> = {
        items: [],
        total: 0,
        page: 1,
        per_page: 50,
        pages: 0,
      };
      
      (apiClient.get as any).mockResolvedValue(mockResponse);

      await inventoryApi.getInventory({ per_page: 50 });

      expect(apiClient.get).toHaveBeenCalledWith('/inventory?per_page=50');
    });
  });

  describe('updateInventory', () => {
    it('should call PUT /inventory/:id', async () => {
      const updateData: InventoryUpdate = {
        quantity: 150,
      };
      
      const mockResponse: Inventory = {
        id: 1,
        product_id: 1,
        product_name: 'Test Product',
        product_sku: 'TEST-001',
        warehouse_id: 1,
        warehouse_name: 'Main Warehouse',
        quantity: 150,
        reorder_level: 10,
        last_updated: '2024-07-01T12:00:00Z',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-07-01T12:00:00Z',
      };
      
      (apiClient.put as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.updateInventory(1, updateData);

      expect(apiClient.put).toHaveBeenCalledWith('/inventory/1', updateData);
      expect(result.quantity).toBe(150);
    });

    it('should update quantity to zero', async () => {
      const updateData: InventoryUpdate = {
        quantity: 0,
      };
      
      const mockResponse: Inventory = {
        id: 1,
        product_id: 1,
        product_name: 'Test Product',
        product_sku: 'TEST-001',
        warehouse_id: 1,
        warehouse_name: 'Main Warehouse',
        quantity: 0,
        reorder_level: 10,
        last_updated: '2024-07-01T12:00:00Z',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-07-01T12:00:00Z',
      };
      
      (apiClient.put as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.updateInventory(1, updateData);

      expect(result.quantity).toBe(0);
    });

    it('should update large inventory quantities', async () => {
      const updateData: InventoryUpdate = {
        quantity: 5000,
      };
      
      const mockResponse: Inventory = {
        id: 1,
        product_id: 1,
        product_name: 'Test Product',
        product_sku: 'TEST-001',
        warehouse_id: 1,
        warehouse_name: 'Main Warehouse',
        quantity: 5000,
        reorder_level: 100,
        last_updated: '2024-07-01T12:00:00Z',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-07-01T12:00:00Z',
      };
      
      (apiClient.put as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.updateInventory(1, updateData);

      expect(result.quantity).toBe(5000);
    });

    it('should handle non-existent inventory record', async () => {
      const updateData: InventoryUpdate = {
        quantity: 100,
      };
      
      const mockError = new Error('Inventory record not found');
      (apiClient.put as any).mockRejectedValue(mockError);

      await expect(
        inventoryApi.updateInventory(999, updateData)
      ).rejects.toThrow('Inventory record not found');
    });

    it('should update last_updated timestamp', async () => {
      const updateData: InventoryUpdate = {
        quantity: 200,
      };
      
      const mockResponse: Inventory = {
        id: 1,
        product_id: 1,
        product_name: 'Test Product',
        product_sku: 'TEST-001',
        warehouse_id: 1,
        warehouse_name: 'Main Warehouse',
        quantity: 200,
        reorder_level: 10,
        last_updated: '2024-07-01T12:30:00Z',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-07-01T12:30:00Z',
      };
      
      (apiClient.put as any).mockResolvedValue(mockResponse);

      const result = await inventoryApi.updateInventory(1, updateData);

      expect(result.last_updated).toBe('2024-07-01T12:30:00Z');
    });
  });

  describe('getLowStockItems', () => {
    it('should call GET /inventory/low-stock', async () => {
      const mockLowStockItems: LowStockItem[] = [
        {
          id: 1,
          product_id: 1,
          product_name: 'Test Product',
          product_sku: 'TEST-001',
          warehouse_id: 1,
          warehouse_name: 'Main Warehouse',
          current_quantity: 5,
          reorder_level: 10,
          supplier_name: 'Acme Corp',
          supplier_lead_time_days: 7,
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockLowStockItems);

      const result = await inventoryApi.getLowStockItems();

      expect(apiClient.get).toHaveBeenCalledWith('/inventory/low-stock');
      expect(result).toEqual(mockLowStockItems);
    });

    it('should return empty array when no low stock items', async () => {
      (apiClient.get as any).mockResolvedValue([]);

      const result = await inventoryApi.getLowStockItems();

      expect(result).toEqual([]);
    });

    it('should return low stock items with supplier details', async () => {
      const mockLowStockItems: LowStockItem[] = [
        {
          id: 1,
          product_id: 1,
          product_name: 'iPhone 15',
          product_sku: 'APL-001',
          warehouse_id: 1,
          warehouse_name: 'US-EAST-WH1',
          current_quantity: 8,
          reorder_level: 50,
          supplier_name: 'Apple Distribution',
          supplier_lead_time_days: 14,
        },
        {
          id: 2,
          product_id: 2,
          product_name: 'Samsung Galaxy',
          product_sku: 'SAM-001',
          warehouse_id: 2,
          warehouse_name: 'US-WEST-WH2',
          current_quantity: 3,
          reorder_level: 30,
          supplier_name: 'Samsung Warehouse',
          supplier_lead_time_days: 10,
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockLowStockItems);

      const result = await inventoryApi.getLowStockItems();

      expect(result).toHaveLength(2);
      expect(result[0].current_quantity).toBeLessThan(result[0].reorder_level);
      expect(result[1].current_quantity).toBeLessThan(result[1].reorder_level);
    });

    it('should handle low stock items without supplier info', async () => {
      const mockLowStockItems: LowStockItem[] = [
        {
          id: 1,
          product_id: 1,
          product_name: 'Test Product',
          product_sku: 'TEST-001',
          warehouse_id: 1,
          warehouse_name: 'Main Warehouse',
          current_quantity: 5,
          reorder_level: 10,
          supplier_name: null,
          supplier_lead_time_days: null,
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockLowStockItems);

      const result = await inventoryApi.getLowStockItems();

      expect(result[0].supplier_name).toBeNull();
      expect(result[0].supplier_lead_time_days).toBeNull();
    });

    it('should identify critical stock levels', async () => {
      const mockLowStockItems: LowStockItem[] = [
        {
          id: 1,
          product_id: 1,
          product_name: 'Critical Product',
          product_sku: 'CRIT-001',
          warehouse_id: 1,
          warehouse_name: 'Main Warehouse',
          current_quantity: 0,
          reorder_level: 20,
          supplier_name: 'Supplier A',
          supplier_lead_time_days: 7,
        },
      ];
      
      (apiClient.get as any).mockResolvedValue(mockLowStockItems);

      const result = await inventoryApi.getLowStockItems();

      expect(result[0].current_quantity).toBe(0);
      expect(result[0].reorder_level).toBe(20);
    });
  });
});
