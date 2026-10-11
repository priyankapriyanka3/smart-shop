/**
 * Supplier types matching backend Pydantic models
 */

export interface SupplierBase {
  name: string;
  contact_name: string;
  email: string;
  phone?: string | null;
  country?: string | null;
  website?: string | null;
  lead_time_days: number;
  rating?: number | null;
}

export interface Supplier extends SupplierBase {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface SupplierCreate extends SupplierBase {}

export interface SupplierUpdate {
  name?: string;
  contact_name?: string;
  email?: string;
  phone?: string | null;
  country?: string | null;
  website?: string | null;
  lead_time_days?: number;
  rating?: number | null;
}
