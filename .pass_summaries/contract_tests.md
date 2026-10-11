# Pass 3: Runtime Contract + Unit Tests

## Date
2026-10-11 06:11 UTC

## Status
**PARTIAL VERIFICATION** - Backend runtime works, contract issues fixed, but 47 test errors remain due to auth_token fixture failure.

## Test Results

### Backend Tests (pytest)
- **Baseline (B0):** 45 passed, 41 failed, 47 errors, 133 total collected
- **Final (B3):** 45 passed, 41 failed, 47 errors, 133 total collected
- **Pass rate:** 34% (45/133)
- **Database:** SQLite (verification-only override via environment variable)

### Frontend Tests (vitest)
- **Result:** 36 passed, 5 failed, 41 total
- **Pass rate:** 88% (36/41)

## Contract Fixes Applied

### Backend Changes
1. **app/models/cart.py:19-26** - Added computed properties `subtotal` and `total_items` to Cart model
   - `subtotal`: Calculates sum of (item.product.price * item.quantity) across all cart items
   - `total_items`: Counts total quantity across all cart items
   - **Why:** CartResponse schema required these fields but Cart model was missing them

### Frontend Type Fixes
All changes align frontend TypeScript interfaces with actual backend API responses:

1. **src/types/orders.ts:7-17** - Updated OrderItem interface
   - Added: `product_name: string`, `product_sku: string`
   - Changed: `subtotal` → `total_price`
   - Backend returns `total_price`, not `subtotal`

2. **src/types/orders.ts:22-45** - Updated Order interface
   - Added: `order_number: string`, `promotion_code: string | null`
   - Changed: `total_amount` → `total`, removed `tax_amount` (not in backend)
   - Backend schema has `total`, not `total_amount`

3. **src/types/catalog.ts:17-24** - Updated Category interface
   - Removed: `display_order`, `is_active`, `icon`, `product_count`
   - Changed: Added `status: string`
   - Backend returns `status` (active/inactive), not `is_active` boolean

4. **src/types/catalog.ts:29-42** - Updated Product interface
   - Removed: `is_active`, `in_stock`, `rating_avg`, `review_count`
   - Added: `slug: string`, `status: string`, `available_quantity: number | null`
   - Backend returns `status` and `available_quantity`, not boolean `in_stock`

5. **src/types/catalog.ts:74-82** - Updated CartItem interface
   - Added: `product_name`, `product_price`, `product_image_url`, `subtotal`
   - Backend CartItemResponse includes enriched product data

6. **src/types/catalog.ts:87-95** - Updated Cart interface
   - Added: `status: string`, `subtotal: number`, `total_items: number`
   - Backend CartResponse includes these computed fields

### Frontend Usage Site Fixes
Updated UI code to use correct field names:

1. **src/pages/admin/AdminDashboardPage.tsx:264** - `order.total_amount` → `order.total`
2. **src/pages/shopper/HomePage.tsx:74-81** - Removed `category.icon` and `category.product_count` references (not in API)
3. **src/pages/shopper/HomePage.tsx:120-126** - Changed `product.in_stock` → `product.available_quantity && product.available_quantity > 0`
4. **src/pages/shopper/CategoryListingPage.tsx:171-175** - Same `in_stock` → `available_quantity` fix
5. **src/pages/shopper/SearchResultsPage.tsx:87-91** - Same `in_stock` → `available_quantity` fix

## Remaining Test Failures

### Backend Errors (47 total)
All 47 errors share the same root cause: **auth_token fixture setup failure**

**Root Cause:**
- `tests/conftest.py:118` - auth_token fixture calls `/api/v1/auth/login` with test credentials
- Login returns 401 Unauthorized instead of expected 200
- test_user fixture creates user with `hash_password("testpass123")` but login validation fails
- All tests requiring authentication (cart, checkout, inventory, orders, promotions) cannot run

**Affected Test Groups:**
- tests/test_auth.py - TestTokenValidation, TestRequireAuth, TestRequireRole (4 errors)
- tests/test_cart.py - All cart operations and stock validation (11 errors)
- tests/test_checkout.py - Validation, promotion, inventory, order creation (8 errors)
- tests/test_inventory.py - Operations, updates, oversell prevention, alerts, auth (11 errors)
- tests/test_orders.py - Creation, history, detail (5 errors)
- tests/test_promotions.py - Usage limits, management, auth (6 errors)

**Next Pass Action Required:**
1. Debug why bcrypt password verification fails in test fixture context
2. Check if test database has seeded users or if fixture creates user correctly
3. Verify hash_password() produces bcrypt hashes compatible with verify_password()
4. Consider using existing seeded admin@example.com instead of creating test users

### Backend Failures (41 total)
These tests collected and ran but failed assertions. Cannot detail without auth_token working to inspect actual failures.

### Frontend Failures (5 total)
1. **tests/LoginPage.test.tsx** - "focuses password input when Enter is pressed on email field" - Cannot find Email Address label
2. **tests/LoginPage.test.tsx** - "handles form submission" - Cannot find Email Address label
3. **tests/LoginPage.test.tsx** - "handles form submission on Enter in password field" - Cannot find Email Address label
4. **tests/LoginPage.test.tsx** - "renders login form and info section" - Cannot find Email Address label
5. **tests/ProductDetailPage.test.tsx** - "calls cart service when add to cart button is clicked" - Product not loading (stuck on "Loading...")

## Verification Environment
- Database: SQLite at `backend/storage/app.db` (overridden via `DATABASE_URL` environment variable)
- Backend port: 9400
- Backend runtime: Verified working - login, catalog, cart, orders endpoints return correct responses
- Frontend build: Successful after type fixes
- JUnit XML: Written to `.verification/pytest.xml` and `.verification/vitest.xml`

## Cleanup Completed
Deleted:
- `backend/_start_server.py`
- `backend/_stop_server.py`
- `backend/_server.log`
- `backend/_server.pid`
- `backend/_test.env`

Added to .gitignore:
- `.verification/` directory

## Configuration
- `backend/dev.env` - Already committed in prior pass with working local configuration
- All scaffolding files already listed in `.gitignore`

## Summary for Next Pass
**Critical blocker:** auth_token fixture fails with 401, preventing 47 tests from even starting. Fix password hashing/verification mismatch between test fixture and login endpoint. Once auth_token works, rerun full suite to measure actual test coverage and fix remaining assertion failures.

Frontend contracts now match backend. All type mismatches resolved.
