# Graph Report - smart-shop  (2026-10-11)

## Corpus Check
- 142 files · ~51,563 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: (none) 5, .db 4, .log 2)

## Summary
- 1625 nodes · 3207 edges · 105 communities (62 shown, 43 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 259 edges (avg confidence: 0.95)
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
- sqlalchemy
- tsconfig.json
- smart-shop-backend
- CatalogService
- User
- Inventory
- services/reviews.py
- OrderService
- RateLimitMiddleware
- CartService
- PaymentService
- activate_promotion
- Cart
- test_seed_acceptance.py
- sqlalchemy_orm
- CheckoutService
- TestAuth
- Acceptance Criteria Verification
- schemas/__init__.py
- login
- App.tsx
- Product
- test_auth_acceptance.py
- InventoryService
- routes/promotions.py
- Audit Logging and GDPR Compliance Implementation Summary
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
- seed_database
- add_to_cart
- types/catalog.ts
- seed.py
- src/shared-config.d.ts
- adjust_stock
- types/shared-config.d.ts
- vite-env.d.ts
- fixture
- TestTokenValidation
- Settings
- security_headers.py
- TestRequireRole
- TestRBAC
- TestStockValidation
- PromotionService
- TestAuditLogging
- Promotion
- start.sh
- Production Deployment Checklist
- TestInventoryOperations
- TestStockUpdates
- TestInventoryAuth
- create_address
- TestPromotionManagement
- TestRequireAuth
- Acceptance Criteria Verification
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
- Review
- Backup and Recovery
- docker-entrypoint.sh
- Smart Shop Deployment Guide
- Production Readiness Verification Report
- Performance Tuning
- Database Configuration
- health_check
- Monitoring and Logging
- Critical Environment Variables
- Scaling Considerations
- Production Deployment
- Additional Verification
- acceptance-checks.sh
- Security Checklist
- launch-test.sh

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
- `Rate Limiting` --references--> `RateLimitMiddleware`  [INFERRED]
  PRODUCTION_READINESS_VERIFICATION.md → backend/app/middleware/rate_limit.py
- `✅ 2. Security Headers Present` --references--> `SecurityHeadersMiddleware`  [INFERRED]
  PRODUCTION_READINESS_VERIFICATION.md → backend/app/middleware/security_headers.py
- `PII Documentation` --references--> `get_pii_fields()`  [INFERRED]
  backend/AUDIT_COMPLIANCE_SUMMARY.md → backend/app/privacy/gdpr.py
- `get_current_user()` --uses--> `User`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customers.py
- `require_auth()` --uses--> `User`  [INFERRED]
  backend/app/auth/dependencies.py → backend/app/models/customers.py

## Import Cycles
- None detected.

## Communities (105 total, 43 thin omitted)

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

### Community 6 - "CustomerService"
Cohesion: 0.11
Nodes (11): register_user(), AddressBase, AddressCreate, AddressListResponse, AddressResponse, AddressUpdate, UserBase, UserCreate (+3 more)

### Community 7 - "sqlalchemy"
Cohesion: 0.11
Nodes (4): run_migrations_offline(), run_migrations_online(), upgrade(), get_db()

### Community 12 - "CatalogService"
Cohesion: 0.06
Nodes (17): Category, get_category(), get_category_by_slug(), get_product(), list_categories(), list_products(), search_products(), CategoryBase (+9 more)

### Community 13 - "User"
Cohesion: 0.12
Nodes (14): hash_password(), Permission, Role, UserRole, User, seed_admin_user(), seed_sample_customers(), admin_user() (+6 more)

### Community 14 - "Inventory"
Cohesion: 0.10
Nodes (4): Inventory, TestCartOperations, TestLowStockAlerts, TestOversellPrevention

### Community 15 - "services/reviews.py"
Cohesion: 0.18
Nodes (5): ReviewAggregateResponse, ReviewBase, ReviewCreate, ReviewListResponse, ReviewModerationRequest

### Community 16 - "OrderService"
Cohesion: 0.05
Nodes (17): Order, OrderItem, get_customer_orders(), get_order(), list_orders(), OrderBase, OrderCreate, OrderDetailResponse (+9 more)

### Community 18 - "CartService"
Cohesion: 0.09
Nodes (9): AddToCartRequest, CartBase, CartItemBase, CartItemCreate, CartItemResponse, CartItemUpdate, CartResponse, UpdateCartItemRequest (+1 more)

### Community 19 - "PaymentService"
Cohesion: 0.10
Nodes (9): Payment, get_order_payments(), get_payment(), PaymentBase, PaymentCreate, PaymentListResponse, PaymentResponse, PaymentStatusUpdate (+1 more)

### Community 20 - "activate_promotion"
Cohesion: 0.15
Nodes (6): activate_promotion(), approve_review(), deactivate_promotion(), get_admin_stats(), reject_review(), update_order_status()

### Community 21 - "Cart"
Cohesion: 0.08
Nodes (9): Cart, CartItem, Address, TestCheckoutValidation, TestInventoryCheck, TestOrderCreation, TestPromotionValidation, TestOrderCreation (+1 more)

### Community 22 - "test_seed_acceptance.py"
Cohesion: 0.10
Nodes (9): test_admin_role_assigned(), test_all_roles_seeded(), test_db(), test_products_seeded(), test_promotions_seeded(), test_reviews_seeded(), test_role_permissions_mapping(), test_seed_idempotent() (+1 more)

### Community 24 - "CheckoutService"
Cohesion: 0.10
Nodes (7): submit_checkout(), validate_checkout(), CheckoutAddress, CheckoutRequest, CheckoutResponse, CheckoutValidationResponse, CheckoutService

### Community 26 - "Acceptance Criteria Verification"
Cohesion: 0.08
Nodes (25): Acceptance Criteria Verification, ✓ Admin Role Assignment, ✓ Admin User Created, ✓ All Roles Seeded, Command Execution, Conclusion, Database Queries, Execution Results (+17 more)

### Community 27 - "schemas/__init__.py"
Cohesion: 0.13
Nodes (12): InventoryBase, InventoryCreate, InventoryListResponse, InventoryUpdate, LowStockResponse, StockAdjustmentRequest, SupplierBase, SupplierCreate (+4 more)

### Community 28 - "login"
Cohesion: 0.20
Nodes (5): Config, login(), LoginRequest, LoginResponse, UserResponse

### Community 29 - "App.tsx"
Cohesion: 0.18
Nodes (13): App(), AuthProvider(), CartPage(), CategoryListingPage(), CheckoutPage(), ProductDetailPage(), SearchResultsPage(), cartService (+5 more)

### Community 30 - "Product"
Cohesion: 0.08
Nodes (6): Product, TestCategoryFilter, TestProductFilters, TestProductList, TestProductSearch, TestProductSorting

### Community 31 - "test_auth_acceptance.py"
Cohesion: 0.05
Nodes (18): create_access_token(), client(), override_get_db(), test_admin_route(), test_client(), test_db(), test_jwt_embeds_string_user_id(), test_login_with_invalid_credentials() (+10 more)

### Community 32 - "InventoryService"
Cohesion: 0.13
Nodes (3): InventoryResponse, ReplenishmentPriorityResponse, InventoryService

### Community 33 - "routes/promotions.py"
Cohesion: 0.11
Nodes (11): create_promotion(), get_promotion(), get_promotion_by_code(), list_promotions(), validate_promotion(), PromotionBase, PromotionCreate, PromotionEligibilityResponse (+3 more)

### Community 34 - "Audit Logging and GDPR Compliance Implementation Summary"
Cohesion: 0.09
Nodes (22): Audit Logging, Audit Logging and GDPR Compliance Implementation Summary, Compliance Requirements Met, Data Anonymization, Database Schema, Database Verification, GDPR Data Privacy Controls, Helper Functions (+14 more)

### Community 35 - "test_audit_compliance.py"
Cohesion: 0.10
Nodes (9): get_audit_logs(), log_audit(), AuditLog, anonymize_user_data(), get_pii_fields(), mask_email(), mask_name(), mask_pii() (+1 more)

### Community 36 - "typing"
Cohesion: 0.09
Nodes (9): get_current_user(), require_auth(), require_permission(), permission_checker(), require_role(), decode_access_token(), verify_password(), check_permission() (+1 more)

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

### Community 48 - "seed_database"
Cohesion: 0.11
Nodes (9): main(), seed_categories(), seed_database(), seed_orders(), seed_products(), seed_promotions(), seed_reviews(), seed_roles() (+1 more)

### Community 49 - "add_to_cart"
Cohesion: 0.14
Nodes (5): add_to_cart(), clear_cart(), get_cart(), remove_cart_item(), update_cart_item()

### Community 50 - "types/catalog.ts"
Cohesion: 0.23
Nodes (10): CategoryCard(), HomePage(), ProductCard(), AddToCartRequest, Cart, CartItem, Category, PaginatedResponse (+2 more)

### Community 51 - "seed.py"
Cohesion: 0.19
Nodes (5): Supplier, Warehouse, seed_inventory(), seed_suppliers(), seed_warehouses()

### Community 53 - "adjust_stock"
Cohesion: 0.19
Nodes (5): adjust_stock(), get_inventory_item(), get_low_stock_alerts(), get_product_availability(), list_inventory()

### Community 56 - "fixture"
Cohesion: 0.08
Nodes (11): admin_token(), auth_token(), client(), db(), expired_promotion(), test_category(), test_inventory(), test_product() (+3 more)

### Community 63 - "PromotionService"
Cohesion: 0.08
Nodes (4): PromotionResponse, PromotionUpdate, PromotionService, TestPromotionEligibility

### Community 65 - "Promotion"
Cohesion: 0.12
Nodes (3): Promotion, TestPromotionDateValidation, TestPromotionTypes

### Community 66 - "start.sh"
Cohesion: 0.47
Nodes (4): check_prerequisites(), DATABASE_URL, find_available_port(), start.sh script

### Community 67 - "Production Deployment Checklist"
Cohesion: 0.18
Nodes (11): Accessibility, Backup & Recovery, Configuration, Database, Documentation, Infrastructure, Monitoring, Performance (+3 more)

### Community 71 - "create_address"
Cohesion: 0.24
Nodes (4): create_address(), get_address(), get_profile(), list_addresses()

### Community 74 - "Acceptance Criteria Verification"
Cohesion: 0.20
Nodes (10): ✅ 10. Accessibility (Additional), ✅ 1. API Response Times, ✅ 3. CORS Configuration, ✅ 4. Error Handling, ✅ 5. Database Indexes, ✅ 6. Dependency Security Scan, ✅ 7. Frontend Page Load Time, ✅ 8. Logging Configuration (+2 more)

### Community 87 - "Backup and Recovery"
Cohesion: 0.22
Nodes (9): Backup and Recovery, Database Backup Strategy, Disaster Recovery Checklist, PostgreSQL Backup, PostgreSQL Restore, Recovery Objectives, Restore Procedures, SQLite Backup (+1 more)

### Community 90 - "Smart Shop Deployment Guide"
Cohesion: 0.25
Nodes (7): Additional Resources, Common Production Issues, Performance Benchmarks, Smart Shop Deployment Guide, Support and Maintenance, Table of Contents, Troubleshooting

### Community 91 - "Production Readiness Verification Report"
Cohesion: 0.25
Nodes (7): Executive Summary, Immediate Actions Before Production Deploy, Performance Benchmarks, Production Readiness Verification Report, Production Recommendations, Scaling Considerations, Summary

### Community 92 - "Performance Tuning"
Cohesion: 0.40
Nodes (5): Backend Performance, Frontend Performance, Load Testing, Performance Tuning, Target Performance Metrics

### Community 93 - "Database Configuration"
Cohesion: 0.40
Nodes (5): Database Configuration, Database Indexes (Configured), Migrations, PostgreSQL (Production Recommended), SQLite (Development/Preview)

### Community 95 - "Monitoring and Logging"
Cohesion: 0.50
Nodes (4): Application Metrics, Health Checks, Monitoring and Logging, Structured Logging

### Community 96 - "Critical Environment Variables"
Cohesion: 0.50
Nodes (4): Backend Environment Variables, Critical Environment Variables, Environment Configuration, Frontend Environment Variables

### Community 97 - "Scaling Considerations"
Cohesion: 0.50
Nodes (4): Caching Layer, Horizontal Scaling, Scaling Considerations, Vertical Scaling

### Community 98 - "Production Deployment"
Cohesion: 0.50
Nodes (4): Container Architecture, Docker Compose (Recommended), Frontend Preview Port, Production Deployment

### Community 99 - "Additional Verification"
Cohesion: 0.50
Nodes (4): Additional Verification, Authentication Security, Rate Limiting, RBAC (Role-Based Access Control)

### Community 101 - "Security Checklist"
Cohesion: 0.67
Nodes (3): Pre-Deployment Security Verification, Security Checklist, Security Headers (Configured)

## Knowledge Gaps
- **252 isolated node(s):** `acceptance-checks.sh script`, `DATABASE_URL`, `Config`, `docker-entrypoint.sh script`, `smart-shop-backend` (+247 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 836 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `TestAuditLogging`, `test_audit_compliance.py`, `typing`, `CustomerService`, `.get_user_by_email`, `Inventory`, `seed_database`, `OrderService`, `seed.py`, `activate_promotion`, `Cart`, `adjust_stock`, `sqlalchemy_orm`, `Review`, `login`, `test_auth_acceptance.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `User` (e.g. with `get_current_user()` and `require_auth()`) actually correct?**
  _`User` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `acceptance-checks.sh script`, `DATABASE_URL`, `Config` to the rest of the system?**
  _252 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Smart Shop` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Why does `PromotionService` connect `PromotionService` to `TestAuditLogging`, `routes/promotions.py`, `Promotion`, `test_audit_compliance.py`, `AdminService`, `Cart`, `sqlalchemy_orm`, `CheckoutService`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `PromotionService` (e.g. with `create_promotion()` and `get_promotion()`) actually correct?**
  _`PromotionService` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._