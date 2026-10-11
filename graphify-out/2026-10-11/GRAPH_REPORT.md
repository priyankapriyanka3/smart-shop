# Graph Report - smart-shop  (2026-10-11)

## Corpus Check
- 137 files · ~46,669 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 5, .db 4, .example 2)

## Summary
- 1529 nodes · 3111 edges · 89 communities (48 shown, 41 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 257 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94e0cf1f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Smart Shop
- package.json
- compilerOptions
- devDependencies
- compilerOptions
- ReviewService
- CustomerService
- seed.py
- tsconfig.json
- smart-shop-backend
- CatalogService
- User
- fixture
- services/reviews.py
- OrderService
- RateLimitMiddleware
- CartService
- PaymentService
- activate_promotion
- Inventory
- seed_database
- main.py
- services/__init__.py
- TestAuth
- Acceptance Criteria Verification
- schemas/__init__.py
- auth.py
- App.tsx
- Product
- test_auth_acceptance.py
- log_audit
- routes/promotions.py
- get_pii_fields
- test_audit_compliance.py
- typing
- scripts
- dependencies
- vite.config.ts
- reviews.ts
- engines
- Card.tsx
- auth-context.tsx
- AdminDashboardPage.tsx
- AdminService
- types/orders.ts
- routes/reviews.py
- services/orders.py
- routes/cart.py
- types/catalog.ts
- create_promotion
- src/shared-config.d.ts
- routes/orders.py
- types/shared-config.d.ts
- vite-env.d.ts
- fixture
- TestTokenValidation
- Settings
- TestProductList
- TestRequireRole
- TestRBAC
- TestStockValidation
- PromotionService
- Session
- Promotion
- start.sh
- TestProductSearch
- TestInventoryOperations
- TestStockUpdates
- TestInventoryAuth
- TestPromotionManagement
- TestRequireAuth
- test_admin_route
- TestCategoryEndpoints
- TestProductDetail
- TestCheckoutAuth
- TestOrderAuth
- stop.sh
- TestPromotionAuth
- TestCartItemUpdate
- TestCartItemRemove
- TestCartAuth
- global_exception_handler
- HelpfulVote
- TestAuditQueryability
- docker-entrypoint.sh

## God Nodes (most connected - your core abstractions)
1. `User` - 70 edges
2. `PromotionService` - 52 edges
3. `Product` - 37 edges
4. `Inventory` - 35 edges
5. `Cart` - 33 edges
6. `Promotion` - 30 edges
7. `OrderService` - 30 edges
8. `ReviewService` - 30 edges
9. `CartItem` - 29 edges
10. `CatalogService` - 29 edges

## Surprising Connections (you probably didn't know these)
- `PII Documentation` --references--> `get_pii_fields()`  [INFERRED]
  backend/AUDIT_COMPLIANCE_SUMMARY.md → backend/app/privacy/gdpr.py
- `get_audit_logs()` --uses--> `AuditLog`  [INFERRED]
  backend/app/audit/logger.py → backend/app/models/audit.py
- `get_current_user()` --uses--> `User`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customers.py
- `require_auth()` --uses--> `User`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customers.py
- `require_role()` --uses--> `User`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customers.py

## Import Cycles
- None detected.

## Communities (89 total, 41 thin omitted)

### Community 0 - "Smart Shop"
Cohesion: 0.05
Nodes (37): Access URLs, Admin Features, API Documentation, Backend, Backend Configuration, Backend Tests, Backend Won't Start, Customer-Facing Features (+29 more)

### Community 1 - "package.json"
Cohesion: 0.09
Nodes (22): name, private, type, version, autoprefixer, clsx, eslint, @eslint/js (+14 more)

### Community 2 - "compilerOptions"
Cohesion: 0.10
Nodes (20): compilerOptions, allowImportingTsExtensions, baseUrl, isolatedModules, jsx, lib, module, moduleDetection (+12 more)

### Community 3 - "devDependencies"
Cohesion: 0.10
Nodes (21): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, jsdom (+13 more)

### Community 4 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, isolatedModules, lib, module, moduleDetection, moduleResolution, noEmit (+8 more)

### Community 5 - "ReviewService"
Cohesion: 0.19
Nodes (3): Review, ReviewResponse, ReviewService

### Community 6 - "CustomerService"
Cohesion: 0.08
Nodes (15): create_address(), get_address(), get_profile(), list_addresses(), register_user(), AddressBase, AddressCreate, AddressListResponse (+7 more)

### Community 7 - "seed.py"
Cohesion: 0.11
Nodes (7): upgrade(), get_db(), Permission, Supplier, seed_roles(), seed_suppliers(), seed_warehouses()

### Community 12 - "CatalogService"
Cohesion: 0.07
Nodes (16): get_category(), get_category_by_slug(), get_product(), list_categories(), list_products(), search_products(), CategoryBase, CategoryCreate (+8 more)

### Community 13 - "User"
Cohesion: 0.09
Nodes (19): hash_password(), Role, UserRole, User, Order, OrderItem, seed_admin_user(), seed_orders() (+11 more)

### Community 14 - "fixture"
Cohesion: 0.22
Nodes (4): client(), override_get_db(), test_client(), test_db()

### Community 15 - "services/reviews.py"
Cohesion: 0.18
Nodes (5): ReviewAggregateResponse, ReviewBase, ReviewCreate, ReviewListResponse, ReviewModerationRequest

### Community 18 - "CartService"
Cohesion: 0.10
Nodes (9): AddToCartRequest, CartBase, CartItemBase, CartItemCreate, CartItemResponse, CartItemUpdate, CartResponse, UpdateCartItemRequest (+1 more)

### Community 19 - "PaymentService"
Cohesion: 0.10
Nodes (9): Payment, get_order_payments(), get_payment(), PaymentBase, PaymentCreate, PaymentListResponse, PaymentResponse, PaymentStatusUpdate (+1 more)

### Community 20 - "activate_promotion"
Cohesion: 0.15
Nodes (6): activate_promotion(), approve_review(), deactivate_promotion(), get_admin_stats(), reject_review(), update_order_status()

### Community 21 - "Inventory"
Cohesion: 0.06
Nodes (13): Cart, CartItem, Address, Inventory, Warehouse, seed_inventory(), TestCheckoutValidation, TestInventoryCheck (+5 more)

### Community 22 - "seed_database"
Cohesion: 0.06
Nodes (15): run_migrations_offline(), run_migrations_online(), main(), seed_database(), seed_promotions(), test_admin_role_assigned(), test_admin_user_seeded(), test_all_roles_seeded() (+7 more)

### Community 23 - "main.py"
Cohesion: 0.11
Nodes (3): health_check(), lifespan(), read_root()

### Community 24 - "services/__init__.py"
Cohesion: 0.13
Nodes (7): submit_checkout(), validate_checkout(), CheckoutAddress, CheckoutRequest, CheckoutResponse, CheckoutValidationResponse, CheckoutService

### Community 26 - "Acceptance Criteria Verification"
Cohesion: 0.08
Nodes (25): Acceptance Criteria Verification, ✓ Admin Role Assignment, ✓ Admin User Created, ✓ All Roles Seeded, Command Execution, Conclusion, Database Queries, Execution Results (+17 more)

### Community 27 - "schemas/__init__.py"
Cohesion: 0.06
Nodes (20): adjust_stock(), get_inventory_item(), get_low_stock_alerts(), get_product_availability(), list_inventory(), InventoryBase, InventoryCreate, InventoryListResponse (+12 more)

### Community 28 - "auth.py"
Cohesion: 0.16
Nodes (6): verify_password(), Config, login(), LoginRequest, LoginResponse, UserResponse

### Community 29 - "App.tsx"
Cohesion: 0.18
Nodes (13): App(), AuthProvider(), CartPage(), CategoryListingPage(), CheckoutPage(), ProductDetailPage(), SearchResultsPage(), cartService (+5 more)

### Community 30 - "Product"
Cohesion: 0.08
Nodes (8): Category, Product, seed_categories(), seed_products(), TestCartOperations, TestCategoryFilter, TestProductFilters, TestProductSorting

### Community 31 - "test_auth_acceptance.py"
Cohesion: 0.06
Nodes (16): get_current_user(), require_auth(), require_role(), create_access_token(), decode_access_token(), test_jwt_embeds_string_user_id(), test_login_with_invalid_credentials(), test_login_with_nonexistent_user() (+8 more)

### Community 32 - "log_audit"
Cohesion: 0.15
Nodes (3): get_audit_logs(), log_audit(), TestAuditLogging

### Community 33 - "routes/promotions.py"
Cohesion: 0.11
Nodes (8): PromotionBase, PromotionCreate, PromotionEligibilityResponse, PromotionListResponse, PromotionResponse, PromotionUpdate, ValidatePromotionRequest, ValidatePromotionResponse

### Community 34 - "get_pii_fields"
Cohesion: 0.07
Nodes (23): get_pii_fields(), Audit Logging, Audit Logging and GDPR Compliance Implementation Summary, Compliance Requirements Met, Data Anonymization, Database Schema, Database Verification, GDPR Data Privacy Controls (+15 more)

### Community 35 - "test_audit_compliance.py"
Cohesion: 0.13
Nodes (6): AuditLog, anonymize_user_data(), mask_email(), mask_name(), mask_pii(), soft_delete_user()

### Community 36 - "typing"
Cohesion: 0.15
Nodes (5): require_permission(), permission_checker(), check_permission(), get_user_permissions(), get_db()

### Community 37 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, preview, test, test:watch, type-check

### Community 38 - "dependencies"
Cohesion: 0.33
Nodes (6): dependencies, clsx, react, react-dom, react-router-dom, tailwind-merge

### Community 40 - "reviews.ts"
Cohesion: 0.19
Nodes (11): AdminHeader(), AdminPromotionsReviewsPage(), getPromotions(), togglePromotionStatus(), approveReview(), getReviews(), rejectReview(), ReviewWithDetails (+3 more)

### Community 41 - "engines"
Cohesion: 0.67
Nodes (3): engines, node, npm

### Community 42 - "Card.tsx"
Cohesion: 0.11
Nodes (21): Badge(), BadgeProps, Button(), ButtonProps, Card(), CardContentProps, CardFooter(), CardFooterProps (+13 more)

### Community 43 - "auth-context.tsx"
Cohesion: 0.11
Nodes (20): RequireAuth(), RequireAuthProps, Header(), AuthContext, AuthContextValue, AuthProviderProps, useAuth(), LoginPage() (+12 more)

### Community 44 - "AdminDashboardPage.tsx"
Cohesion: 0.20
Nodes (11): apiClient, formatCurrency(), AdminDashboardPage(), AdminHeader(), getDashboardStats(), getInventory(), InventoryWithProduct, DashboardStats (+3 more)

### Community 45 - "AdminService"
Cohesion: 0.11
Nodes (3): DashboardResponse, StatsResponse, AdminService

### Community 46 - "types/orders.ts"
Cohesion: 0.18
Nodes (11): OrderHistoryPage(), ordersService, PaginatedResponse, Product, ApiError, PaginatedResponse, Order, OrderCreateRequest (+3 more)

### Community 47 - "routes/reviews.py"
Cohesion: 0.24
Nodes (4): create_review(), get_product_review_summary(), get_review(), list_reviews()

### Community 48 - "services/orders.py"
Cohesion: 0.18
Nodes (6): OrderBase, OrderCreate, OrderItemBase, OrderItemResponse, OrderListResponse, OrderStatusUpdate

### Community 49 - "routes/cart.py"
Cohesion: 0.15
Nodes (5): add_to_cart(), clear_cart(), get_cart(), remove_cart_item(), update_cart_item()

### Community 50 - "types/catalog.ts"
Cohesion: 0.23
Nodes (10): CategoryCard(), HomePage(), ProductCard(), AddToCartRequest, Cart, CartItem, Category, PaginatedResponse (+2 more)

### Community 51 - "create_promotion"
Cohesion: 0.21
Nodes (5): create_promotion(), get_promotion(), get_promotion_by_code(), list_promotions(), validate_promotion()

### Community 53 - "routes/orders.py"
Cohesion: 0.23
Nodes (4): get_customer_orders(), get_order(), list_orders(), OrderDetailResponse

### Community 56 - "fixture"
Cohesion: 0.08
Nodes (11): admin_token(), auth_token(), client(), db(), expired_promotion(), test_category(), test_inventory(), test_product() (+3 more)

### Community 65 - "Promotion"
Cohesion: 0.09
Nodes (4): Promotion, TestPromotionDateValidation, TestPromotionTypes, TestPromotionUsageLimits

### Community 66 - "start.sh"
Cohesion: 0.47
Nodes (4): check_prerequisites(), DATABASE_URL, find_available_port(), start.sh script

## Knowledge Gaps
- **190 isolated node(s):** `Config`, `docker-entrypoint.sh script`, `smart-shop-backend`, `name`, `private` (+185 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 766 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `log_audit`, `Promotion`, `Session`, `test_audit_compliance.py`, `typing`, `CustomerService`, `seed.py`, `test_admin_route`, `OrderService`, `activate_promotion`, `Inventory`, `TestAuditQueryability`, `schemas/__init__.py`, `auth.py`, `test_auth_acceptance.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `User` (e.g. with `get_current_user()` and `require_auth()`) actually correct?**
  _`User` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `docker-entrypoint.sh script`, `smart-shop-backend` to the rest of the system?**
  _190 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Smart Shop` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Why does `PromotionService` connect `PromotionService` to `log_audit`, `routes/promotions.py`, `Promotion`, `test_audit_compliance.py`, `seed.py`, `AdminService`, `create_promotion`, `services/__init__.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `PromotionService` (e.g. with `create_promotion()` and `get_promotion()`) actually correct?**
  _`PromotionService` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._