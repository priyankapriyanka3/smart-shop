"""
Idempotent seed script for Smart Shop.

Populates:
- Default admin user (admin@example.com / admin123)
- Roles (admin, inventory_manager, customer_support, customer) with permission mappings
- 100+ products across 50+ categories with realistic names/descriptions/prices
- 3-5 warehouses
- 10-20 suppliers
- 5-10 sample customers
- Sample inventory records
- Sample promotions
- Sample reviews
- Sample orders

Checks for existing data before inserting to ensure idempotency.
Can be run from main.py lifespan hook or directly via python3 app/seed.py
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.customers import User, Address
from app.models.admin import Role, Permission, UserRole
from app.models.catalog import Category, Product
from app.models.inventory import Warehouse, Supplier, Inventory
from app.models.promotions import Promotion
from app.models.reviews import Review
from app.models.orders import Order, OrderItem
from app.models.payments import Payment
from app.auth.password import hash_password


def seed_database(db_session):
    """Run all seed operations idempotently."""
    print("Starting seed script...")
    
    # 1. Seed Roles
    seed_roles(db_session)
    
    # 2. Seed Default Admin User
    seed_admin_user(db_session)
    
    # 3. Seed Sample Customers
    seed_sample_customers(db_session)
    
    # 4. Seed Categories (50+)
    seed_categories(db_session)
    
    # 5. Seed Warehouses (3-5)
    seed_warehouses(db_session)
    
    # 6. Seed Suppliers (10-20)
    seed_suppliers(db_session)
    
    # 7. Seed Products (100+)
    seed_products(db_session)
    
    # 8. Seed Inventory Records
    seed_inventory(db_session)
    
    # 9. Seed Promotions
    seed_promotions(db_session)
    
    # 10. Seed Reviews
    seed_reviews(db_session)
    
    # 11. Seed Sample Orders
    seed_orders(db_session)
    
    print("Seed script completed successfully!")


def seed_roles(db_session):
    """Seed roles with permissions matching ROLE_PERMISSIONS map in auth/rbac.py."""
    print("Seeding roles...")
    
    roles_data = [
        {
            "name": "admin",
            "description": "Administrator with full system access",
            "permissions": [
                ("products", "create"), ("products", "read"), ("products", "update"), ("products", "delete"),
                ("categories", "create"), ("categories", "read"), ("categories", "update"), ("categories", "delete"),
                ("orders", "create"), ("orders", "read"), ("orders", "update"), ("orders", "delete"),
                ("inventory", "create"), ("inventory", "read"), ("inventory", "update"), ("inventory", "delete"),
                ("promotions", "create"), ("promotions", "read"), ("promotions", "update"), ("promotions", "delete"),
                ("reviews", "read"), ("reviews", "approve"), ("reviews", "reject"), ("reviews", "delete"),
                ("users", "create"), ("users", "read"), ("users", "update"), ("users", "delete"),
                ("warehouses", "create"), ("warehouses", "read"), ("warehouses", "update"), ("warehouses", "delete"),
                ("suppliers", "create"), ("suppliers", "read"), ("suppliers", "update"), ("suppliers", "delete"),
                ("audit", "read"),
                ("dashboard", "read"),
            ]
        },
        {
            "name": "inventory_manager",
            "description": "Manages inventory, warehouses, and suppliers",
            "permissions": [
                ("products", "read"),
                ("categories", "read"),
                ("inventory", "create"), ("inventory", "read"), ("inventory", "update"), ("inventory", "delete"),
                ("warehouses", "create"), ("warehouses", "read"), ("warehouses", "update"),
                ("suppliers", "create"), ("suppliers", "read"), ("suppliers", "update"),
                ("orders", "read"),
            ]
        },
        {
            "name": "customer_support",
            "description": "Handles customer orders, reviews, and support",
            "permissions": [
                ("orders", "read"), ("orders", "update"),
                ("users", "read"),
                ("products", "read"),
                ("categories", "read"),
                ("reviews", "read"), ("reviews", "approve"), ("reviews", "reject"),
                ("promotions", "read"),
            ]
        },
        {
            "name": "customer",
            "description": "Regular customer with shopping and account management access",
            "permissions": [
                ("products", "read"),
                ("categories", "read"),
                ("cart", "create"), ("cart", "read"), ("cart", "update"), ("cart", "delete"),
                ("orders", "create"), ("orders", "read"),
                ("reviews", "create"), ("reviews", "read"),
                ("profile", "read"), ("profile", "update"),
                ("addresses", "create"), ("addresses", "read"), ("addresses", "update"), ("addresses", "delete"),
            ]
        }
    ]
    
    for role_data in roles_data:
        # Check if role exists
        existing_role = db_session.query(Role).filter_by(name=role_data["name"]).first()
        if not existing_role:
            role = Role(name=role_data["name"], description=role_data["description"])
            db_session.add(role)
            db_session.flush()
            
            # Add permissions
            for resource, action in role_data["permissions"]:
                permission = Permission(role_id=role.id, resource=resource, action=action)
                db_session.add(permission)
            
            print(f"  Created role: {role_data['name']} with {len(role_data['permissions'])} permissions")
        else:
            print(f"  Role already exists: {role_data['name']}")
    
    db_session.commit()


def seed_admin_user(db_session):
    """Seed default admin user with credentials admin@example.com / admin123."""
    print("Seeding admin user...")
    
    # Check if admin exists
    existing_admin = db_session.query(User).filter_by(email="admin@example.com").first()
    if not existing_admin:
        admin_password_hash = hash_password("admin123")
        admin_user = User(
            email="admin@example.com",
            name="Admin User",
            password_hash=admin_password_hash,
            status="active",
            consent_timestamp=datetime.utcnow()
        )
        db_session.add(admin_user)
        db_session.flush()
        
        # Assign admin role
        admin_role = db_session.query(Role).filter_by(name="admin").first()
        if admin_role:
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db_session.add(user_role)
        
        db_session.commit()
        print(f"  Created admin user: admin@example.com with admin role")
    else:
        print("  Admin user already exists")


def seed_sample_customers(db_session):
    """Seed 5-10 sample customers with realistic data."""
    print("Seeding sample customers...")
    
    customers_data = [
        {"email": "john.doe@example.com", "name": "John Doe"},
        {"email": "jane.smith@example.com", "name": "Jane Smith"},
        {"email": "bob.johnson@example.com", "name": "Bob Johnson"},
        {"email": "alice.williams@example.com", "name": "Alice Williams"},
        {"email": "charlie.brown@example.com", "name": "Charlie Brown"},
        {"email": "diana.garcia@example.com", "name": "Diana Garcia"},
        {"email": "edward.martinez@example.com", "name": "Edward Martinez"},
        {"email": "fiona.rodriguez@example.com", "name": "Fiona Rodriguez"},
    ]
    
    customer_role = db_session.query(Role).filter_by(name="customer").first()
    
    for customer_data in customers_data:
        existing_customer = db_session.query(User).filter_by(email=customer_data["email"]).first()
        if not existing_customer:
            password_hash = hash_password("customer123")
            customer = User(
                email=customer_data["email"],
                name=customer_data["name"],
                password_hash=password_hash,
                status="active",
                consent_timestamp=datetime.utcnow()
            )
            db_session.add(customer)
            db_session.flush()
            
            # Assign customer role
            if customer_role:
                user_role = UserRole(user_id=customer.id, role_id=customer_role.id)
                db_session.add(user_role)
            
            # Add sample address
            address = Address(
                user_id=customer.id,
                address_type="shipping",
                street=f"{100 + customer.id} Main Street",
                city="San Francisco",
                state_province="CA",
                postal_code="94102",
                country="USA",
                is_default=True
            )
            db_session.add(address)
            
            print(f"  Created customer: {customer_data['email']}")
    
    db_session.commit()


def seed_categories(db_session):
    """Seed 50+ categories with hierarchical structure."""
    print("Seeding categories...")
    
    # Count existing categories
    existing_count = db_session.query(Category).count()
    if existing_count >= 50:
        print(f"  Categories already seeded ({existing_count} exist)")
        return
    
    categories_data = [
        # Electronics (10)
        {"name": "Electronics", "slug": "electronics", "parent": None},
        {"name": "Laptops & Computers", "slug": "laptops-computers", "parent": "Electronics"},
        {"name": "Smartphones & Tablets", "slug": "smartphones-tablets", "parent": "Electronics"},
        {"name": "Audio & Headphones", "slug": "audio-headphones", "parent": "Electronics"},
        {"name": "Cameras & Photography", "slug": "cameras-photography", "parent": "Electronics"},
        {"name": "Wearable Technology", "slug": "wearable-technology", "parent": "Electronics"},
        {"name": "Gaming Consoles", "slug": "gaming-consoles", "parent": "Electronics"},
        {"name": "Computer Accessories", "slug": "computer-accessories", "parent": "Electronics"},
        {"name": "Smart Home Devices", "slug": "smart-home-devices", "parent": "Electronics"},
        {"name": "Television & Video", "slug": "television-video", "parent": "Electronics"},
        
        # Home & Kitchen (10)
        {"name": "Home & Kitchen", "slug": "home-kitchen", "parent": None},
        {"name": "Kitchen Appliances", "slug": "kitchen-appliances", "parent": "Home & Kitchen"},
        {"name": "Cookware & Bakeware", "slug": "cookware-bakeware", "parent": "Home & Kitchen"},
        {"name": "Home Decor", "slug": "home-decor", "parent": "Home & Kitchen"},
        {"name": "Furniture", "slug": "furniture", "parent": "Home & Kitchen"},
        {"name": "Bedding & Bath", "slug": "bedding-bath", "parent": "Home & Kitchen"},
        {"name": "Storage & Organization", "slug": "storage-organization", "parent": "Home & Kitchen"},
        {"name": "Lighting", "slug": "lighting", "parent": "Home & Kitchen"},
        {"name": "Kitchen Utensils", "slug": "kitchen-utensils", "parent": "Home & Kitchen"},
        {"name": "Dining & Entertaining", "slug": "dining-entertaining", "parent": "Home & Kitchen"},
        
        # Fashion & Apparel (10)
        {"name": "Fashion & Apparel", "slug": "fashion-apparel", "parent": None},
        {"name": "Men's Clothing", "slug": "mens-clothing", "parent": "Fashion & Apparel"},
        {"name": "Women's Clothing", "slug": "womens-clothing", "parent": "Fashion & Apparel"},
        {"name": "Kids' Clothing", "slug": "kids-clothing", "parent": "Fashion & Apparel"},
        {"name": "Shoes", "slug": "shoes", "parent": "Fashion & Apparel"},
        {"name": "Accessories", "slug": "accessories", "parent": "Fashion & Apparel"},
        {"name": "Jewelry & Watches", "slug": "jewelry-watches", "parent": "Fashion & Apparel"},
        {"name": "Handbags & Wallets", "slug": "handbags-wallets", "parent": "Fashion & Apparel"},
        {"name": "Sunglasses", "slug": "sunglasses", "parent": "Fashion & Apparel"},
        {"name": "Athletic Wear", "slug": "athletic-wear", "parent": "Fashion & Apparel"},
        
        # Sports & Outdoors (10)
        {"name": "Sports & Outdoors", "slug": "sports-outdoors", "parent": None},
        {"name": "Fitness Equipment", "slug": "fitness-equipment", "parent": "Sports & Outdoors"},
        {"name": "Camping & Hiking", "slug": "camping-hiking", "parent": "Sports & Outdoors"},
        {"name": "Cycling", "slug": "cycling", "parent": "Sports & Outdoors"},
        {"name": "Water Sports", "slug": "water-sports", "parent": "Sports & Outdoors"},
        {"name": "Team Sports", "slug": "team-sports", "parent": "Sports & Outdoors"},
        {"name": "Golf Equipment", "slug": "golf-equipment", "parent": "Sports & Outdoors"},
        {"name": "Yoga & Pilates", "slug": "yoga-pilates", "parent": "Sports & Outdoors"},
        {"name": "Running & Jogging", "slug": "running-jogging", "parent": "Sports & Outdoors"},
        {"name": "Winter Sports", "slug": "winter-sports", "parent": "Sports & Outdoors"},
        
        # Beauty & Personal Care (10)
        {"name": "Beauty & Personal Care", "slug": "beauty-personal-care", "parent": None},
        {"name": "Skincare", "slug": "skincare", "parent": "Beauty & Personal Care"},
        {"name": "Makeup", "slug": "makeup", "parent": "Beauty & Personal Care"},
        {"name": "Hair Care", "slug": "hair-care", "parent": "Beauty & Personal Care"},
        {"name": "Fragrances", "slug": "fragrances", "parent": "Beauty & Personal Care"},
        {"name": "Personal Hygiene", "slug": "personal-hygiene", "parent": "Beauty & Personal Care"},
        {"name": "Oral Care", "slug": "oral-care", "parent": "Beauty & Personal Care"},
        {"name": "Bath & Body", "slug": "bath-body", "parent": "Beauty & Personal Care"},
        {"name": "Nail Care", "slug": "nail-care", "parent": "Beauty & Personal Care"},
        {"name": "Men's Grooming", "slug": "mens-grooming", "parent": "Beauty & Personal Care"},
        
        # Books & Media (5)
        {"name": "Books & Media", "slug": "books-media", "parent": None},
        {"name": "Books", "slug": "books", "parent": "Books & Media"},
        {"name": "Music", "slug": "music", "parent": "Books & Media"},
        {"name": "Movies & TV", "slug": "movies-tv", "parent": "Books & Media"},
        {"name": "Video Games", "slug": "video-games", "parent": "Books & Media"},
    ]
    
    # Create parent categories first, then children
    parent_map = {}
    
    for cat_data in categories_data:
        existing_cat = db_session.query(Category).filter_by(slug=cat_data["slug"]).first()
        if not existing_cat:
            parent_id = None
            if cat_data["parent"]:
                parent_cat = parent_map.get(cat_data["parent"])
                if parent_cat:
                    parent_id = parent_cat.id
            
            category = Category(
                name=cat_data["name"],
                slug=cat_data["slug"],
                description=f"{cat_data['name']} products and accessories",
                parent_id=parent_id,
                status="active"
            )
            db_session.add(category)
            db_session.flush()
            parent_map[cat_data["name"]] = category
    
    db_session.commit()
    print(f"  Created {len(categories_data)} categories")


def seed_warehouses(db_session):
    """Seed 3-5 warehouses."""
    print("Seeding warehouses...")
    
    warehouses_data = [
        {"name": "West Coast Distribution", "code": "WC-01", "location": "San Francisco, CA"},
        {"name": "East Coast Hub", "code": "EC-01", "location": "New York, NY"},
        {"name": "Central Fulfillment", "code": "CF-01", "location": "Chicago, IL"},
        {"name": "Southern Distribution", "code": "SD-01", "location": "Dallas, TX"},
    ]
    
    for wh_data in warehouses_data:
        existing_wh = db_session.query(Warehouse).filter_by(code=wh_data["code"]).first()
        if not existing_wh:
            warehouse = Warehouse(
                name=wh_data["name"],
                code=wh_data["code"],
                location=wh_data["location"],
                status="active"
            )
            db_session.add(warehouse)
            print(f"  Created warehouse: {wh_data['name']}")
    
    db_session.commit()


def seed_suppliers(db_session):
    """Seed 10-20 suppliers."""
    print("Seeding suppliers...")
    
    suppliers_data = [
        {"name": "TechSupply Corp", "code": "SUP-001", "email": "contact@techsupply.com", "lead_time": 7},
        {"name": "ElectroMax Ltd", "code": "SUP-002", "email": "orders@electromax.com", "lead_time": 5},
        {"name": "HomeGoods Inc", "code": "SUP-003", "email": "sales@homegoods.com", "lead_time": 10},
        {"name": "Fashion Forward", "code": "SUP-004", "email": "info@fashionforward.com", "lead_time": 14},
        {"name": "Sports Gear Pro", "code": "SUP-005", "email": "support@sportsgear.com", "lead_time": 7},
        {"name": "Beauty Essentials", "code": "SUP-006", "email": "orders@beautyessentials.com", "lead_time": 5},
        {"name": "Book Distributors", "code": "SUP-007", "email": "contact@bookdist.com", "lead_time": 3},
        {"name": "Kitchen Masters", "code": "SUP-008", "email": "sales@kitchenmasters.com", "lead_time": 12},
        {"name": "Outdoor Adventures", "code": "SUP-009", "email": "info@outdooradv.com", "lead_time": 9},
        {"name": "Tech Innovations", "code": "SUP-010", "email": "orders@techinnovations.com", "lead_time": 6},
        {"name": "Furniture World", "code": "SUP-011", "email": "sales@furnitureworld.com", "lead_time": 21},
        {"name": "Apparel Hub", "code": "SUP-012", "email": "contact@apparelhub.com", "lead_time": 10},
        {"name": "Gaming Central", "code": "SUP-013", "email": "support@gamingcentral.com", "lead_time": 5},
        {"name": "Audio Specialists", "code": "SUP-014", "email": "orders@audiospec.com", "lead_time": 7},
        {"name": "Smart Home Tech", "code": "SUP-015", "email": "info@smarthometech.com", "lead_time": 8},
    ]
    
    for sup_data in suppliers_data:
        existing_sup = db_session.query(Supplier).filter_by(code=sup_data["code"]).first()
        if not existing_sup:
            supplier = Supplier(
                name=sup_data["name"],
                code=sup_data["code"],
                contact_email=sup_data["email"],
                lead_time_days=sup_data["lead_time"],
                status="active"
            )
            db_session.add(supplier)
            print(f"  Created supplier: {sup_data['name']}")
    
    db_session.commit()


def seed_products(db_session):
    """Seed 100+ products across categories with realistic data."""
    print("Seeding products...")
    
    # Count existing products
    existing_count = db_session.query(Product).count()
    if existing_count >= 100:
        print(f"  Products already seeded ({existing_count} exist)")
        return
    
    # Get categories
    categories = db_session.query(Category).filter(Category.parent_id.isnot(None)).all()
    if not categories:
        print("  No categories found, cannot seed products")
        return
    
    # Product templates by category slug
    product_templates = {
        "laptops-computers": [
            ("Dell XPS 13 Laptop", "High-performance ultrabook with Intel Core i7, 16GB RAM, 512GB SSD", 1299.99),
            ("MacBook Air M2", "Apple MacBook Air with M2 chip, 13-inch display, 256GB storage", 1199.99),
            ("HP Pavilion Desktop", "Desktop computer with AMD Ryzen 5, 8GB RAM, 1TB HDD", 699.99),
            ("ASUS ROG Gaming Laptop", "Gaming laptop with NVIDIA RTX 3060, 15.6-inch 144Hz display", 1599.99),
            ("Lenovo ThinkPad X1", "Business laptop with Intel Core i5, 8GB RAM, 256GB SSD", 999.99),
        ],
        "smartphones-tablets": [
            ("iPhone 14 Pro", "Apple iPhone 14 Pro with 128GB storage, ProMotion display", 999.99),
            ("Samsung Galaxy S23", "Samsung flagship phone with 256GB storage, 50MP camera", 899.99),
            ("iPad Pro 11-inch", "Apple iPad Pro with M2 chip, 128GB, Wi-Fi", 799.99),
            ("Google Pixel 7", "Google Pixel 7 with Tensor G2 chip, 128GB storage", 599.99),
            ("Samsung Galaxy Tab S8", "Android tablet with 11-inch display, S Pen included", 649.99),
        ],
        "audio-headphones": [
            ("Sony WH-1000XM5", "Premium noise-canceling wireless headphones", 399.99),
            ("Apple AirPods Pro", "Wireless earbuds with active noise cancellation", 249.99),
            ("Bose QuietComfort 45", "Wireless noise-canceling headphones", 329.99),
            ("JBL Flip 6", "Portable Bluetooth speaker, waterproof", 129.99),
            ("Sennheiser HD 599", "Open-back audiophile headphones", 199.99),
        ],
        "cameras-photography": [
            ("Canon EOS R6", "Full-frame mirrorless camera with 20.1MP sensor", 2499.99),
            ("Sony Alpha a7 IV", "Full-frame hybrid camera with 33MP sensor", 2499.99),
            ("Nikon D850", "Professional DSLR camera with 45.7MP sensor", 2999.99),
            ("GoPro Hero 11", "Action camera with 5.3K video recording", 399.99),
            ("DJI Mini 3 Pro", "Foldable drone with 4K HDR video", 759.99),
        ],
        "wearable-technology": [
            ("Apple Watch Series 8", "Smartwatch with health tracking, GPS", 399.99),
            ("Fitbit Charge 5", "Fitness tracker with heart rate monitor", 149.99),
            ("Samsung Galaxy Watch 5", "Android smartwatch with fitness features", 279.99),
            ("Garmin Forerunner 255", "GPS running smartwatch", 349.99),
            ("Oura Ring Gen 3", "Sleep and health tracking ring", 299.99),
        ],
        "kitchen-appliances": [
            ("KitchenAid Stand Mixer", "5-quart tilt-head stand mixer, 10 speeds", 279.99),
            ("Ninja Air Fryer", "6-quart air fryer with digital controls", 119.99),
            ("Cuisinart Coffee Maker", "12-cup programmable coffee maker", 79.99),
            ("Instant Pot Duo", "7-in-1 electric pressure cooker, 6 quart", 99.99),
            ("Vitamix E310 Blender", "Professional-grade blender, 48oz container", 349.99),
        ],
        "cookware-bakeware": [
            ("All-Clad Stainless Steel Cookware Set", "10-piece cookware set", 599.99),
            ("Le Creuset Dutch Oven", "5.5-quart enameled cast iron dutch oven", 379.99),
            ("Nordic Ware Baking Sheet", "Half sheet aluminum baking pan", 19.99),
            ("Lodge Cast Iron Skillet", "12-inch pre-seasoned cast iron skillet", 34.99),
            ("Pyrex Glass Baking Dish Set", "3-piece glass baking dish set", 29.99),
        ],
        "furniture": [
            ("IKEA KALLAX Shelf Unit", "4x4 cube storage shelf, white", 149.99),
            ("West Elm Mid-Century Sofa", "82-inch modern sofa in performance velvet", 1799.99),
            ("Herman Miller Aeron Chair", "Ergonomic office chair, size B", 1395.00),
            ("Pottery Barn Dining Table", "Extending dining table, seats 6-8", 999.99),
            ("Wayfair Platform Bed Frame", "Queen size upholstered platform bed", 399.99),
        ],
        "mens-clothing": [
            ("Levi's 501 Original Jeans", "Classic straight fit denim jeans", 69.99),
            ("Nike Dri-FIT T-Shirt", "Athletic fit performance t-shirt", 29.99),
            ("Patagonia Down Jacket", "Men's down sweater hoody", 279.00),
            ("Ralph Lauren Oxford Shirt", "Classic fit button-down shirt", 89.50),
            ("Adidas Ultraboost Shoes", "Running shoes with boost cushioning", 180.00),
        ],
        "womens-clothing": [
            ("Lululemon Align Leggings", "High-rise yoga pants, 25-inch", 98.00),
            ("Zara Blazer", "Structured blazer with shoulder pads", 89.90),
            ("H&M Cotton Dress", "Midi-length A-line dress", 39.99),
            ("Everlane Cashmere Sweater", "Crew neck cashmere sweater", 100.00),
            ("Nike Air Max Sneakers", "Women's lifestyle sneakers", 120.00),
        ],
        "fitness-equipment": [
            ("Bowflex Adjustable Dumbbells", "SelectTech 552 dumbbells, 5-52.5 lbs", 349.00),
            ("Peloton Bike+", "Indoor cycling bike with touchscreen", 2495.00),
            ("Yoga Mat Premium", "6mm thick non-slip exercise mat", 49.99),
            ("TRX Suspension Trainer", "Home suspension training system", 169.95),
            ("PowerBlock Dumbbells", "Adjustable dumbbell set, 50 lbs", 299.00),
        ],
        "skincare": [
            ("CeraVe Moisturizing Cream", "Face and body moisturizer, 19 oz", 18.99),
            ("The Ordinary Niacinamide", "10% Niacinamide + 1% Zinc serum", 5.90),
            ("Neutrogena Sunscreen SPF 50", "Ultra sheer dry-touch sunscreen", 11.99),
            ("La Roche-Posay Cleanser", "Toleriane hydrating gentle cleanser", 14.99),
            ("Drunk Elephant Vitamin C", "C-Firma day serum, 1 oz", 80.00),
        ],
        "books": [
            ("The Great Gatsby", "F. Scott Fitzgerald classic novel", 14.99),
            ("Atomic Habits", "James Clear - habit formation guide", 16.99),
            ("Where the Crawdads Sing", "Delia Owens bestselling novel", 15.99),
            ("Sapiens", "Yuval Noah Harari - brief history of humankind", 19.99),
            ("The Midnight Library", "Matt Haig - contemporary fiction", 17.00),
        ],
    }
    
    product_counter = 0
    for category in categories:
        if category.slug in product_templates:
            templates = product_templates[category.slug]
            for name, description, price in templates:
                # Generate SKU
                sku = f"SKU-{category.slug.upper()[:5]}-{product_counter:04d}"
                slug = f"{name.lower().replace(' ', '-')}-{product_counter}"
                
                existing_product = db_session.query(Product).filter_by(sku=sku).first()
                if not existing_product:
                    product = Product(
                        category_id=category.id,
                        sku=sku,
                        name=name,
                        slug=slug,
                        brand=name.split()[0] if ' ' in name else "Generic",
                        description=description,
                        price=price,
                        image_url=f"https://via.placeholder.com/400x400?text={name.split()[0]}",
                        status="active"
                    )
                    db_session.add(product)
                    product_counter += 1
        
        # Add some generic products to reach 100+
        if product_counter < 100:
            for i in range(3):
                sku = f"SKU-{category.slug.upper()[:5]}-{product_counter:04d}"
                slug = f"{category.slug}-product-{product_counter}"
                name = f"{category.name} Item {i+1}"
                
                existing_product = db_session.query(Product).filter_by(sku=sku).first()
                if not existing_product:
                    product = Product(
                        category_id=category.id,
                        sku=sku,
                        name=name,
                        slug=slug,
                        brand="Generic",
                        description=f"Quality {category.name.lower()} product",
                        price=round(29.99 + (i * 10.0), 2),
                        image_url=f"https://via.placeholder.com/400x400?text=Product",
                        status="active"
                    )
                    db_session.add(product)
                    product_counter += 1
                
                if product_counter >= 120:
                    break
        
        if product_counter >= 120:
            break
    
    db_session.commit()
    print(f"  Created {product_counter} products")


def seed_inventory(db_session):
    """Seed inventory records for products in warehouses."""
    print("Seeding inventory...")
    
    products = db_session.query(Product).all()
    warehouses = db_session.query(Warehouse).all()
    suppliers = db_session.query(Supplier).all()
    
    if not products or not warehouses or not suppliers:
        print("  Missing prerequisites for inventory seeding")
        return
    
    inventory_count = 0
    for product in products[:100]:  # First 100 products
        # Add inventory to 1-2 warehouses per product
        for warehouse in warehouses[:2]:
            existing_inv = db_session.query(Inventory).filter_by(
                product_id=product.id,
                warehouse_id=warehouse.id
            ).first()
            
            if not existing_inv:
                # Random quantity between 0 and 100
                quantity = (product.id * 7) % 101
                reorder_level = 10
                
                # Determine status based on quantity
                if quantity == 0:
                    status = "out_of_stock"
                elif quantity <= reorder_level:
                    status = "low_stock"
                else:
                    status = "in_stock"
                
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    supplier_id=suppliers[product.id % len(suppliers)].id,
                    quantity=quantity,
                    reorder_level=reorder_level,
                    status=status
                )
                db_session.add(inventory)
                inventory_count += 1
    
    db_session.commit()
    print(f"  Created {inventory_count} inventory records")


def seed_promotions(db_session):
    """Seed sample promotions with valid date ranges and usage limits."""
    print("Seeding promotions...")
    
    now = datetime.utcnow()
    
    promotions_data = [
        {
            "code": "SAVE10",
            "name": "10% off your entire order",
            "discount_type": "percentage",
            "discount_value": 10.0,
            "start_date": now - timedelta(days=7),
            "end_date": now + timedelta(days=30),
            "minimum_order_amount": 50.0,
            "max_uses": 1000,
            "status": "active"
        },
        {
            "code": "FREESHIP",
            "name": "Free shipping on orders over $75",
            "discount_type": "free_shipping",
            "discount_value": 0.0,
            "start_date": now - timedelta(days=14),
            "end_date": now + timedelta(days=60),
            "minimum_order_amount": 75.0,
            "max_uses": 500,
            "status": "active"
        },
        {
            "code": "WELCOME20",
            "name": "$20 off first order",
            "discount_type": "fixed",
            "discount_value": 20.0,
            "start_date": now - timedelta(days=1),
            "end_date": now + timedelta(days=90),
            "minimum_order_amount": 100.0,
            "max_uses": 100,
            "status": "active"
        },
        {
            "code": "FLASH25",
            "name": "25% off flash sale",
            "discount_type": "percentage",
            "discount_value": 25.0,
            "start_date": now - timedelta(days=30),
            "end_date": now - timedelta(days=15),
            "minimum_order_amount": 0.0,
            "max_uses": 50,
            "status": "expired"
        },
        {
            "code": "SUMMER15",
            "name": "15% off summer collection",
            "discount_type": "percentage",
            "discount_value": 15.0,
            "start_date": now + timedelta(days=7),
            "end_date": now + timedelta(days=60),
            "minimum_order_amount": 75.0,
            "max_uses": 200,
            "status": "inactive"
        },
    ]
    
    for promo_data in promotions_data:
        existing_promo = db_session.query(Promotion).filter_by(code=promo_data["code"]).first()
        if not existing_promo:
            promotion = Promotion(**promo_data)
            db_session.add(promotion)
            print(f"  Created promotion: {promo_data['code']}")
    
    db_session.commit()


def seed_reviews(db_session):
    """Seed sample reviews linked to products and customers."""
    print("Seeding reviews...")
    
    products = db_session.query(Product).limit(20).all()
    customers = db_session.query(User).join(UserRole).join(Role).filter(Role.name == "customer").limit(8).all()
    
    if not products or not customers:
        print("  Missing products or customers for review seeding")
        return
    
    review_texts = [
        "Great product! Exactly what I was looking for.",
        "Good quality but a bit pricey.",
        "Exceeded my expectations. Highly recommend!",
        "Decent product, works as advertised.",
        "Not worth the price, disappointed with quality.",
        "Amazing! Best purchase I've made this year.",
        "Average product, nothing special.",
        "Excellent value for money.",
        "Could be better, but it gets the job done.",
        "Outstanding quality and fast delivery!",
    ]
    
    review_count = 0
    for i, product in enumerate(products):
        # Add 2-3 reviews per product
        num_reviews = 2 if i % 2 == 0 else 3
        for j in range(num_reviews):
            customer = customers[(i + j) % len(customers)]
            
            existing_review = db_session.query(Review).filter_by(
                product_id=product.id,
                customer_id=customer.id
            ).first()
            
            if not existing_review:
                rating = 4 if (i + j) % 3 == 0 else 5
                review = Review(
                    product_id=product.id,
                    customer_id=customer.id,
                    rating=rating,
                    review_text=review_texts[(i + j) % len(review_texts)],
                    status="approved"
                )
                db_session.add(review)
                review_count += 1
    
    db_session.commit()
    print(f"  Created {review_count} reviews")


def seed_orders(db_session):
    """Seed sample orders for customers."""
    print("Seeding orders...")
    
    # Check if orders already exist
    existing_count = db_session.query(Order).count()
    if existing_count > 0:
        print(f"  Orders already seeded ({existing_count} exist)")
        return
    
    customers = db_session.query(User).join(UserRole).join(Role).filter(Role.name == "customer").limit(5).all()
    products = db_session.query(Product).limit(10).all()
    
    if not customers or not products:
        print("  Missing customers or products for order seeding")
        return
    
    order_count = 0
    for i, customer in enumerate(customers):
        # Get customer's default address
        address = db_session.query(Address).filter_by(user_id=customer.id, is_default=True).first()
        if not address:
            continue
        
        # Create 1-2 orders per customer
        num_orders = 1 if i % 2 == 0 else 2
        for j in range(num_orders):
            order_number = f"ORD-{customer.id:04d}-{j:02d}-{i:04d}"
            order = Order(
                customer_id=customer.id,
                order_number=order_number,
                status="completed" if j == 0 else "processing",
                subtotal=0.0,
                discount_amount=0.0,
                shipping_cost=9.99,
                total=0.0,
                shipping_street=address.street,
                shipping_city=address.city,
                shipping_state_province=address.state_province,
                shipping_postal_code=address.postal_code,
                shipping_country=address.country,
                billing_street=address.street,
                billing_city=address.city,
                billing_state_province=address.state_province,
                billing_postal_code=address.postal_code,
                billing_country=address.country
            )
            db_session.add(order)
            db_session.flush()
            
            # Add 2-3 items to the order
            order_subtotal = 0.0
            for k in range(2 if j == 0 else 3):
                product = products[(i + j + k) % len(products)]
                quantity = 1 if k == 0 else 2
                unit_price = product.price
                total_price = unit_price * quantity
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                db_session.add(order_item)
                order_subtotal += total_price
            
            # Update order totals
            order.subtotal = order_subtotal
            order.total = order_subtotal + order.shipping_cost
            
            # Create payment record
            payment = Payment(
                order_id=order.id,
                amount=order.total,
                currency="USD",
                payment_method="credit_card",
                status="completed" if j == 0 else "pending",
                external_reference=f"PAY-{order.id:08d}"
            )
            db_session.add(payment)
            
            order_count += 1
    
    db_session.commit()
    print(f"  Created {order_count} orders")


def main():
    """Main entry point when run directly."""
    import os
    from app.config import settings
    
    # Use database URL from environment or default to SQLite
    database_url = os.environ.get('DATABASE_URL', settings.database_url)
    
    # Create engine and session
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Run seed operations
    db_session = SessionLocal()
    try:
        seed_database(db_session)
    except Exception as e:
        print(f"Error during seeding: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
