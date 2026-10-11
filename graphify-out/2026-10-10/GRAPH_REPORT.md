# Graph Report - smart-shop  (2026-10-10)

## Corpus Check
- 132 files · ~31,813 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 2, .tsbuildinfo 2, .example 1)

## Summary
- 1048 nodes · 2087 edges · 58 communities (32 shown, 26 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 155 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94e0cf1f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Smart Shop
- package.json
- compilerOptions
- test_auth.py
- compilerOptions
- discounts.py
- test_cart.py
- database.py
- CartService
- tsconfig.json
- smart-shop-backend
- test_products.py
- fixture
- products.py
- ProductService
- categories.py
- list_products
- client.ts
- routes/auth.py
- discount_service.py
- schemas/supplier.py
- .get_category_hierarchy
- MockPaymentProvider
- test_discounts.py
- test_inventory_service.py
- schemas/discount.py
- schemas/__init__.py
- update_order_status
- Customer
- Product
- dependencies.py
- routes/cart.py
- App.tsx
- format.ts
- hash_password
- AuditLog
- test_jwt.py
- create_review
- main.py
- start.sh
- 6a13b344fd09_initial_database_schema.py
- update_inventory
- Settings
- run_migrations_offline
- run_migrations_online
- get_cart_service
- remove_cart_item
- get_product_service
- stop.sh
- docker-entrypoint.sh

## God Nodes (most connected - your core abstractions)
1. `Product` - 36 edges
2. `ProductService` - 36 edges
3. `Customer` - 28 edges
4. `CartService` - 23 edges
5. `Inventory` - 21 edges
6. `AuditLog` - 17 edges
7. `compilerOptions` - 17 edges
8. `get_db()` - 16 edges
9. `Category` - 16 edges
10. `PaginatedResponse` - 16 edges

## Surprising Connections (you probably didn't know these)
- `get_current_user()` --uses--> `Customer`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customer.py
- `require_role()` --uses--> `Customer`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customer.py
- `CartService` --uses--> `Cart`  [INFERRED]
  backend/app/services/cart_service.py → backend/app/models/cart.py
- `ProductService` --uses--> `Category`  [INFERRED]
  backend/app/services/product_service.py → backend/app/models/category.py
- `sample_category()` --uses--> `Category`  [INFERRED]
  backend/tests/conftest.py → backend/app/models/category.py

## Import Cycles
- None detected.

## Communities (58 total, 26 thin omitted)

### Community 0 - "Smart Shop"
Cohesion: 0.05
Nodes (40): Accessibility, Admin Features, Architecture, Backend, Backend Container, Backup and Recovery, Building Images for Production, Customer Features (+32 more)

### Community 1 - "package.json"
Cohesion: 0.04
Nodes (46): dependencies, react, react-dom, react-router-dom, devDependencies, autoprefixer, eslint, @eslint/js (+38 more)

### Community 2 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleDetection, moduleResolution (+10 more)

### Community 3 - "test_auth.py"
Cohesion: 0.05
Nodes (17): test_get_current_user(), test_get_current_user_invalid_token(), test_get_current_user_unauthorized(), test_login_nonexistent_user(), test_login_success(), test_login_wrong_password(), test_register_duplicate_email(), test_register_short_password() (+9 more)

### Community 4 - "compilerOptions"
Cohesion: 0.12
Nodes (15): compilerOptions, allowImportingTsExtensions, isolatedModules, lib, module, moduleDetection, moduleResolution, noEmit (+7 more)

### Community 6 - "test_cart.py"
Cohesion: 0.08
Nodes (11): test_add_duplicate_item_increments_quantity(), test_add_item_inactive_product(), test_add_item_insufficient_stock(), test_add_item_to_cart(), test_get_cart_with_items(), test_get_empty_cart(), test_remove_cart_item(), test_remove_cart_item_not_found() (+3 more)

### Community 8 - "CartService"
Cohesion: 0.10
Nodes (3): CartItem, CartItemCreate, CartService

### Community 15 - "test_products.py"
Cohesion: 0.08
Nodes (12): test_activate_product(), test_create_product(), test_create_product_invalid_category(), test_deactivate_product(), test_filter_products_by_category(), test_get_product_by_id(), test_get_product_not_found(), test_list_products_empty() (+4 more)

### Community 16 - "fixture"
Cohesion: 0.12
Nodes (7): auth_headers(), client(), sample_category(), sample_customer(), sample_inventory(), sample_product(), test_db()

### Community 17 - "products.py"
Cohesion: 0.15
Nodes (8): activate_product(), create_product(), deactivate_product(), update_product(), ProductBase, ProductCreate, ProductResponse, ProductUpdate

### Community 19 - "categories.py"
Cohesion: 0.15
Nodes (7): get_category(), get_product_service(), list_categories(), list_category_products(), CategoryBase, CategoryList, CategoryResponse

### Community 20 - "list_products"
Cohesion: 0.18
Nodes (3): get_product(), list_products(), search_products()

### Community 21 - "client.ts"
Cohesion: 0.06
Nodes (43): cartApi, apiClient, ApiError, request(), discountsApi, inventoryApi, ordersApi, productsApi (+35 more)

### Community 22 - "routes/auth.py"
Cohesion: 0.14
Nodes (10): get_current_user_profile(), login(), register(), update_profile(), Config, LoginRequest, ProfileUpdateRequest, RegisterRequest (+2 more)

### Community 23 - "discount_service.py"
Cohesion: 0.19
Nodes (7): Discount, create_discount(), get_all_discounts(), get_discount_by_id(), increment_discount_usage(), update_discount(), validate_discount()

### Community 24 - "schemas/supplier.py"
Cohesion: 0.13
Nodes (7): create_supplier(), get_supplier(), list_suppliers(), update_supplier(), SupplierCreate, SupplierResponse, SupplierUpdate

### Community 26 - "MockPaymentProvider"
Cohesion: 0.06
Nodes (8): get_payment_service(), MockPaymentProvider, PaymentOutcome, PaymentProvider, PaymentService, TestMockPaymentProvider, TestPaymentOutcome, TestPaymentService

### Community 28 - "test_discounts.py"
Cohesion: 0.10
Nodes (9): override_get_db(), setup_database(), test_actor(), test_create_discount(), test_discount(), test_list_discounts(), test_validate_discount_min_order(), test_validate_discount_not_found() (+1 more)

### Community 29 - "test_inventory_service.py"
Cohesion: 0.07
Nodes (18): Category, Inventory, Warehouse, get_inventory_by_id(), get_inventory_records(), get_low_stock_items(), update_inventory_quantity(), sample_warehouse() (+10 more)

### Community 30 - "schemas/discount.py"
Cohesion: 0.12
Nodes (9): create_discount(), list_discounts(), update_discount(), validate_discount(), DiscountCreate, DiscountResponse, DiscountUpdate, DiscountValidationRequest (+1 more)

### Community 31 - "schemas/__init__.py"
Cohesion: 0.10
Nodes (10): InventoryResponse, InventoryUpdate, LowStockItem, OrderItemResponse, OrderNoteCreate, OrderResponse, OrderStatusUpdate, ReviewCreate (+2 more)

### Community 32 - "update_order_status"
Cohesion: 0.18
Nodes (4): add_order_note(), get_order(), list_orders(), update_order_status()

### Community 33 - "Customer"
Cohesion: 0.13
Nodes (10): init_db(), Customer, Review, main(), seed_database(), create_review(), get_aggregate_rating(), get_product_reviews() (+2 more)

### Community 34 - "Product"
Cohesion: 0.07
Nodes (17): OrderItem, Order, Product, add_order_note(), get_all_orders(), get_customer_orders(), get_order_by_id(), update_order_status() (+9 more)

### Community 36 - "routes/cart.py"
Cohesion: 0.14
Nodes (9): add_cart_item(), get_cart(), get_current_customer_id(), update_cart_item(), CartItemBase, CartItemResponse, CartItemUpdate, CartResponse (+1 more)

### Community 37 - "App.tsx"
Cohesion: 0.07
Nodes (53): authApi, categoriesApi, getCategories(), getProduct(), getProducts(), getProductReviews(), App(), Breadcrumb() (+45 more)

### Community 39 - "hash_password"
Cohesion: 0.18
Nodes (7): hash_password(), verify_password(), test_hash_different_passwords(), test_hash_password(), test_verify_password_correct(), test_verify_password_empty(), test_verify_password_incorrect()

### Community 40 - "AuditLog"
Cohesion: 0.22
Nodes (6): AuditLog, Supplier, create_supplier(), get_all_suppliers(), get_supplier_by_id(), update_supplier()

### Community 41 - "test_jwt.py"
Cohesion: 0.15
Nodes (8): create_access_token(), decode_access_token(), test_create_access_token(), test_decode_access_token_expired(), test_decode_access_token_invalid(), test_decode_access_token_valid(), test_different_roles(), test_token_contains_expiry()

### Community 42 - "create_review"
Cohesion: 0.16
Nodes (5): create_review(), get_product_rating(), hide_review(), list_product_reviews(), mark_review_helpful()

### Community 45 - "start.sh"
Cohesion: 0.53
Nodes (5): check_prerequisites(), DATABASE_URL, find_available_port(), portable_sed(), start.sh script

### Community 47 - "update_inventory"
Cohesion: 0.25
Nodes (3): get_low_stock(), list_inventory(), update_inventory()

## Knowledge Gaps
- **132 isolated node(s):** `Config`, `smart-shop-backend`, `docker-entrypoint.sh script`, `name`, `private` (+127 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 515 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Product` connect `Product` to `Customer`, `test_cart.py`, `database.py`, `CartService`, `test_products.py`, `fixture`, `products.py`, `ProductService`, `test_inventory_service.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Product` (e.g. with `CartService` and `get_inventory_by_id()`) actually correct?**
  _`Product` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `smart-shop-backend`, `docker-entrypoint.sh script` to the rest of the system?**
  _132 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Smart Shop` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `ProductService` connect `ProductService` to `Product`, `discounts.py`, `products.py`, `categories.py`, `list_products`, `get_product_service`, `.get_category_hierarchy`, `test_inventory_service.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `ProductService` (e.g. with `get_category()` and `list_categories()`) actually correct?**
  _`ProductService` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.041666666666666664 - nodes in this community are weakly interconnected._