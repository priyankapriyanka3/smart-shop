/**
 * Category types matching backend Pydantic models
 */

export interface CategoryBase {
  name: string;
  description: string;
  parent_id?: number | null;
}

export interface Category extends CategoryBase {
  id: number;
  is_active: boolean; // Backend returns boolean
  subcategories?: Category[]; // Backend returns subcategories, not children
  created_at: string;
  updated_at: string;
}

export interface CategoryCreate extends CategoryBase {}

export interface CategoryUpdate {
  name?: string;
  description?: string;
  parent_id?: number | null;
}
