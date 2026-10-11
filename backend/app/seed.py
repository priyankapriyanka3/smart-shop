"""
Idempotent seed script for Smart Shop database.
Populates categories, products, warehouses, suppliers, promotions, reviews, and default users.
"""
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.auth.password import hash_password
from app.database import SessionLocal, init_db
from app.models.category import Category
from app.models.customer import Customer
from app.models.discount import Discount
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.review import Review
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse


def seed_database(db: Session):
    """
    Seed the database with initial data.
    Idempotent - checks if data exists before inserting.
    """
    print("Starting database seeding...")

    # Check if already seeded
    existing_customer = db.query(Customer).filter(Customer.email == "admin@example.com").first()
    if existing_customer:
        print("Database already seeded. Skipping.")
        return

    # === Seed Default Users ===
    print("Seeding default users...")
    users = [
        Customer(
            email="admin@example.com",
            password_hash=hash_password("Admin123!"),
            full_name="Admin User",
            role="admin",
            is_active=True
        ),
        Customer(
            email="customer@example.com",
            password_hash=hash_password("Customer123!"),
            full_name="Test Customer",
            role="shopper",
            is_active=True
        ),
        Customer(
            email="inventory@example.com",
            password_hash=hash_password("Inventory123!"),
            full_name="Inventory Manager",
            role="inventory_manager",
            is_active=True
        ),
        Customer(
            email="support@example.com",
            password_hash=hash_password("Support123!"),
            full_name="Customer Support",
            role="customer_support",
            is_active=True
        ),
    ]
    for user in users:
        db.add(user)
    db.commit()
    print(f"  Created {len(users)} users")

    # === Seed Categories ===
    print("Seeding categories...")

    # Top-level categories
    electronics = Category(name="Electronics", description="Electronic devices and accessories", is_active=True)
    clothing = Category(name="Clothing", description="Apparel and fashion", is_active=True)
    home = Category(name="Home & Kitchen", description="Home goods and kitchen appliances", is_active=True)
    books = Category(name="Books", description="Books and reading materials", is_active=True)
    sports = Category(name="Sports & Outdoors", description="Sports equipment and outdoor gear", is_active=True)
    beauty = Category(name="Beauty & Personal Care", description="Beauty products and personal care items", is_active=True)
    toys = Category(name="Toys & Games", description="Toys, games, and puzzles", is_active=True)
    automotive = Category(name="Automotive", description="Car parts and accessories", is_active=True)

    db.add_all([electronics, clothing, home, books, sports, beauty, toys, automotive])
    db.commit()

    # Sub-categories for Electronics
    computers = Category(name="Computers & Tablets", parent_id=electronics.id, is_active=True)
    phones = Category(name="Mobile Phones", parent_id=electronics.id, is_active=True)
    audio = Category(name="Audio & Headphones", parent_id=electronics.id, is_active=True)
    cameras = Category(name="Cameras & Photography", parent_id=electronics.id, is_active=True)
    gaming = Category(name="Gaming", parent_id=electronics.id, is_active=True)
    wearables = Category(name="Wearables", parent_id=electronics.id, is_active=True)

    # Sub-categories for Clothing
    mens = Category(name="Men's Clothing", parent_id=clothing.id, is_active=True)
    womens = Category(name="Women's Clothing", parent_id=clothing.id, is_active=True)
    kids = Category(name="Kids' Clothing", parent_id=clothing.id, is_active=True)
    shoes = Category(name="Shoes", parent_id=clothing.id, is_active=True)
    accessories = Category(name="Accessories", parent_id=clothing.id, is_active=True)

    # Sub-categories for Home & Kitchen
    furniture = Category(name="Furniture", parent_id=home.id, is_active=True)
    kitchen_appliances = Category(name="Kitchen Appliances", parent_id=home.id, is_active=True)
    bedding = Category(name="Bedding", parent_id=home.id, is_active=True)
    decor = Category(name="Home Decor", parent_id=home.id, is_active=True)

    # Sub-categories for Books
    fiction = Category(name="Fiction", parent_id=books.id, is_active=True)
    nonfiction = Category(name="Non-Fiction", parent_id=books.id, is_active=True)
    childrens_books = Category(name="Children's Books", parent_id=books.id, is_active=True)

    # Sub-categories for Sports & Outdoors
    fitness = Category(name="Fitness Equipment", parent_id=sports.id, is_active=True)
    camping = Category(name="Camping & Hiking", parent_id=sports.id, is_active=True)
    cycling = Category(name="Cycling", parent_id=sports.id, is_active=True)

    # Sub-categories for Beauty
    skincare = Category(name="Skincare", parent_id=beauty.id, is_active=True)
    makeup = Category(name="Makeup", parent_id=beauty.id, is_active=True)
    haircare = Category(name="Hair Care", parent_id=beauty.id, is_active=True)

    # Sub-categories for Toys
    action_figures = Category(name="Action Figures", parent_id=toys.id, is_active=True)
    board_games = Category(name="Board Games", parent_id=toys.id, is_active=True)
    educational = Category(name="Educational Toys", parent_id=toys.id, is_active=True)

    all_subcategories = [
        computers, phones, audio, cameras, gaming, wearables,
        mens, womens, kids, shoes, accessories,
        furniture, kitchen_appliances, bedding, decor,
        fiction, nonfiction, childrens_books,
        fitness, camping, cycling,
        skincare, makeup, haircare,
        action_figures, board_games, educational
    ]

    db.add_all(all_subcategories)
    db.commit()
    print(f"  Created {8 + len(all_subcategories)} categories")

    # === Seed Warehouses ===
    print("Seeding warehouses...")
    warehouse_east = Warehouse(name="East Coast Distribution", location="New York, NY")
    warehouse_west = Warehouse(name="West Coast Distribution", location="Los Angeles, CA")
    db.add_all([warehouse_east, warehouse_west])
    db.commit()
    print("  Created 2 warehouses")

    # === Seed Suppliers ===
    print("Seeding suppliers...")
    suppliers_data = [
        {"name": "TechGlobal Inc", "contact_name": "John Smith", "email": "john@techglobal.com", "phone": "555-0101", "country": "USA", "lead_time_days": 7},
        {"name": "FashionWorld Ltd", "contact_name": "Sarah Johnson", "email": "sarah@fashionworld.com", "phone": "555-0102", "country": "Italy", "lead_time_days": 14},
        {"name": "HomeComfort Co", "contact_name": "Mike Williams", "email": "mike@homecomfort.com", "phone": "555-0103", "country": "China", "lead_time_days": 21},
        {"name": "BookMasters", "contact_name": "Emily Brown", "email": "emily@bookmasters.com", "phone": "555-0104", "country": "UK", "lead_time_days": 10},
        {"name": "SportsPro Supply", "contact_name": "David Lee", "email": "david@sportspro.com", "phone": "555-0105", "country": "Germany", "lead_time_days": 12},
        {"name": "BeautySource", "contact_name": "Lisa Chen", "email": "lisa@beautysource.com", "phone": "555-0106", "country": "France", "lead_time_days": 15},
        {"name": "ToyFactory Direct", "contact_name": "Tom Anderson", "email": "tom@toyfactory.com", "phone": "555-0107", "country": "Japan", "lead_time_days": 18},
        {"name": "AutoParts Plus", "contact_name": "James Wilson", "email": "james@autoparts.com", "phone": "555-0108", "country": "USA", "lead_time_days": 5},
        {"name": "ElectroSupply Co", "contact_name": "Anna Martinez", "email": "anna@electrosupply.com", "phone": "555-0109", "country": "Taiwan", "lead_time_days": 20},
        {"name": "Quality Goods Ltd", "contact_name": "Robert Garcia", "email": "robert@qualitygoods.com", "phone": "555-0110", "country": "Canada", "lead_time_days": 8},
    ]

    suppliers = [Supplier(**data) for data in suppliers_data]
    db.add_all(suppliers)
    db.commit()
    print(f"  Created {len(suppliers)} suppliers")

    # === Seed Products ===
    print("Seeding products...")
    products_data = [
        # Electronics - Computers
        {"name": "Premium Laptop 15-inch", "brand": "TechMaster", "sku": "LPT-001", "price": Decimal("999.99"), "description": "High-performance laptop with 16GB RAM and 512GB SSD", "category_id": computers.id},
        {"name": "Business Ultrabook", "brand": "ProTech", "sku": "LPT-002", "price": Decimal("1299.99"), "description": "Lightweight ultrabook perfect for professionals", "category_id": computers.id},
        {"name": "Gaming Laptop Pro", "brand": "GameRig", "sku": "LPT-003", "price": Decimal("1899.99"), "description": "High-end gaming laptop with RTX graphics", "category_id": computers.id},
        {"name": "Tablet 10-inch", "brand": "TechMaster", "sku": "TAB-001", "price": Decimal("449.99"), "description": "Versatile tablet for work and entertainment", "category_id": computers.id},
        {"name": "2-in-1 Convertible", "brand": "ProTech", "sku": "TAB-002", "price": Decimal("799.99"), "description": "Laptop and tablet in one device", "category_id": computers.id},

        # Electronics - Mobile Phones
        {"name": "Smartphone Pro Max", "brand": "PhoneCorp", "sku": "PHN-001", "price": Decimal("1199.99"), "description": "Latest flagship smartphone with 5G", "category_id": phones.id},
        {"name": "Budget Smartphone", "brand": "ValuePhone", "sku": "PHN-002", "price": Decimal("299.99"), "description": "Affordable smartphone with great features", "category_id": phones.id},
        {"name": "Foldable Phone", "brand": "PhoneCorp", "sku": "PHN-003", "price": Decimal("1799.99"), "description": "Innovative foldable display technology", "category_id": phones.id},

        # Electronics - Audio
        {"name": "Wireless Headphones Premium", "brand": "AudioTech", "sku": "AUD-001", "price": Decimal("349.99"), "description": "Noise-cancelling wireless headphones", "category_id": audio.id},
        {"name": "Bluetooth Speaker", "brand": "SoundWave", "sku": "AUD-002", "price": Decimal("129.99"), "description": "Portable waterproof speaker", "category_id": audio.id},
        {"name": "Gaming Headset RGB", "brand": "GameAudio", "sku": "AUD-003", "price": Decimal("179.99"), "description": "7.1 surround sound gaming headset", "category_id": audio.id},
        {"name": "True Wireless Earbuds", "brand": "AudioTech", "sku": "AUD-004", "price": Decimal("199.99"), "description": "Premium earbuds with active noise cancellation", "category_id": audio.id},

        # Electronics - Cameras
        {"name": "DSLR Camera Pro", "brand": "PhotoMaster", "sku": "CAM-001", "price": Decimal("1499.99"), "description": "Professional DSLR camera body", "category_id": cameras.id},
        {"name": "Mirrorless Camera", "brand": "PhotoTech", "sku": "CAM-002", "price": Decimal("1299.99"), "description": "Compact mirrorless camera with 4K video", "category_id": cameras.id},
        {"name": "Action Camera", "brand": "ActionPro", "sku": "CAM-003", "price": Decimal("399.99"), "description": "Waterproof action camera for adventures", "category_id": cameras.id},

        # Electronics - Gaming
        {"name": "Gaming Console Next-Gen", "brand": "GameStation", "sku": "GAM-001", "price": Decimal("499.99"), "description": "Latest generation gaming console", "category_id": gaming.id},
        {"name": "Gaming Controller Pro", "brand": "GameStation", "sku": "GAM-002", "price": Decimal("79.99"), "description": "Wireless controller with haptic feedback", "category_id": gaming.id},
        {"name": "VR Headset", "brand": "VirtualTech", "sku": "GAM-003", "price": Decimal("599.99"), "description": "Immersive virtual reality headset", "category_id": gaming.id},

        # Electronics - Wearables
        {"name": "Smartwatch Pro", "brand": "WearTech", "sku": "WER-001", "price": Decimal("399.99"), "description": "Advanced smartwatch with health tracking", "category_id": wearables.id},
        {"name": "Fitness Tracker Band", "brand": "FitTrack", "sku": "WER-002", "price": Decimal("149.99"), "description": "Slim fitness tracker with heart rate monitor", "category_id": wearables.id},

        # Clothing - Men's
        {"name": "Men's Cotton T-Shirt", "brand": "ComfortWear", "sku": "MNS-001", "price": Decimal("29.99"), "description": "Classic cotton t-shirt in multiple colors", "category_id": mens.id},
        {"name": "Men's Jeans Classic Fit", "brand": "DenimCo", "sku": "MNS-002", "price": Decimal("69.99"), "description": "Comfortable classic fit jeans", "category_id": mens.id},
        {"name": "Men's Dress Shirt", "brand": "FormalStyle", "sku": "MNS-003", "price": Decimal("59.99"), "description": "Professional dress shirt", "category_id": mens.id},
        {"name": "Men's Hoodie", "brand": "StreetStyle", "sku": "MNS-004", "price": Decimal("79.99"), "description": "Warm and comfortable hoodie", "category_id": mens.id},

        # Clothing - Women's
        {"name": "Women's Summer Dress", "brand": "FashionPlus", "sku": "WMN-001", "price": Decimal("89.99"), "description": "Elegant summer dress", "category_id": womens.id},
        {"name": "Women's Yoga Pants", "brand": "ActiveFit", "sku": "WMN-002", "price": Decimal("49.99"), "description": "Stretchy and comfortable yoga pants", "category_id": womens.id},
        {"name": "Women's Blouse", "brand": "ChicStyle", "sku": "WMN-003", "price": Decimal("54.99"), "description": "Stylish blouse for any occasion", "category_id": womens.id},
        {"name": "Women's Cardigan", "brand": "CozyKnits", "sku": "WMN-004", "price": Decimal("64.99"), "description": "Soft knit cardigan", "category_id": womens.id},

        # Clothing - Kids
        {"name": "Kids T-Shirt Pack (3)", "brand": "KidStyle", "sku": "KDS-001", "price": Decimal("34.99"), "description": "Pack of 3 colorful kids t-shirts", "category_id": kids.id},
        {"name": "Kids Jeans", "brand": "LittleDenim", "sku": "KDS-002", "price": Decimal("39.99"), "description": "Durable kids jeans", "category_id": kids.id},
        {"name": "Kids Winter Jacket", "brand": "WarmKids", "sku": "KDS-003", "price": Decimal("79.99"), "description": "Insulated winter jacket", "category_id": kids.id},

        # Clothing - Shoes
        {"name": "Running Shoes Pro", "brand": "SportFeet", "sku": "SHO-001", "price": Decimal("119.99"), "description": "Professional running shoes", "category_id": shoes.id},
        {"name": "Casual Sneakers", "brand": "StreetFeet", "sku": "SHO-002", "price": Decimal("79.99"), "description": "Comfortable everyday sneakers", "category_id": shoes.id},
        {"name": "Dress Shoes Leather", "brand": "FormalFeet", "sku": "SHO-003", "price": Decimal("149.99"), "description": "Classic leather dress shoes", "category_id": shoes.id},
        {"name": "Hiking Boots", "brand": "TrailMaster", "sku": "SHO-004", "price": Decimal("159.99"), "description": "Waterproof hiking boots", "category_id": shoes.id},

        # Clothing - Accessories
        {"name": "Leather Belt", "brand": "StylePlus", "sku": "ACC-001", "price": Decimal("39.99"), "description": "Genuine leather belt", "category_id": accessories.id},
        {"name": "Winter Scarf", "brand": "WarmStyle", "sku": "ACC-002", "price": Decimal("29.99"), "description": "Soft wool blend scarf", "category_id": accessories.id},
        {"name": "Baseball Cap", "brand": "CapStyle", "sku": "ACC-003", "price": Decimal("24.99"), "description": "Adjustable baseball cap", "category_id": accessories.id},

        # Home & Kitchen - Furniture
        {"name": "Office Chair Ergonomic", "brand": "ComfortSeats", "sku": "FUR-001", "price": Decimal("299.99"), "description": "Ergonomic office chair with lumbar support", "category_id": furniture.id},
        {"name": "Bookshelf 5-Tier", "brand": "HomeStorage", "sku": "FUR-002", "price": Decimal("149.99"), "description": "Modern 5-tier bookshelf", "category_id": furniture.id},
        {"name": "Coffee Table Wood", "brand": "WoodCraft", "sku": "FUR-003", "price": Decimal("249.99"), "description": "Solid wood coffee table", "category_id": furniture.id},

        # Home & Kitchen - Appliances
        {"name": "Coffee Maker Automatic", "brand": "BrewMaster", "sku": "APP-001", "price": Decimal("89.99"), "description": "Programmable coffee maker", "category_id": kitchen_appliances.id},
        {"name": "Blender High-Speed", "brand": "BlendTech", "sku": "APP-002", "price": Decimal("129.99"), "description": "Professional blender with multiple settings", "category_id": kitchen_appliances.id},
        {"name": "Air Fryer XL", "brand": "CookPro", "sku": "APP-003", "price": Decimal("149.99"), "description": "Large capacity air fryer", "category_id": kitchen_appliances.id},
        {"name": "Toaster 4-Slice", "brand": "ToastMaster", "sku": "APP-004", "price": Decimal("59.99"), "description": "Extra-wide slot toaster", "category_id": kitchen_appliances.id},

        # Home & Kitchen - Bedding
        {"name": "Sheet Set Queen", "brand": "SleepWell", "sku": "BED-001", "price": Decimal("69.99"), "description": "Soft microfiber sheet set", "category_id": bedding.id},
        {"name": "Comforter King", "brand": "CozyNights", "sku": "BED-002", "price": Decimal("129.99"), "description": "All-season down alternative comforter", "category_id": bedding.id},
        {"name": "Pillow Memory Foam (2)", "brand": "DreamComfort", "sku": "BED-003", "price": Decimal("79.99"), "description": "Set of 2 memory foam pillows", "category_id": bedding.id},

        # Home & Kitchen - Decor
        {"name": "Wall Art Canvas Set", "brand": "ArtStyle", "sku": "DEC-001", "price": Decimal("99.99"), "description": "3-piece canvas wall art", "category_id": decor.id},
        {"name": "Table Lamp Modern", "brand": "LightStyle", "sku": "DEC-002", "price": Decimal("54.99"), "description": "Contemporary table lamp", "category_id": decor.id},
        {"name": "Throw Pillows Set (4)", "brand": "ComfyHome", "sku": "DEC-003", "price": Decimal("49.99"), "description": "Decorative throw pillows", "category_id": decor.id},

        # Books - Fiction
        {"name": "Mystery Novel Bestseller", "brand": "ReadWell Publishing", "sku": "FIC-001", "price": Decimal("24.99"), "description": "Gripping mystery thriller", "category_id": fiction.id},
        {"name": "Science Fiction Epic", "brand": "SciFi Press", "sku": "FIC-002", "price": Decimal("29.99"), "description": "Award-winning sci-fi novel", "category_id": fiction.id},
        {"name": "Romance Novel Collection", "brand": "HeartStory Books", "sku": "FIC-003", "price": Decimal("34.99"), "description": "3-book romance collection", "category_id": fiction.id},

        # Books - Non-Fiction
        {"name": "Business Strategy Guide", "brand": "Success Press", "sku": "NFC-001", "price": Decimal("39.99"), "description": "Comprehensive business strategy book", "category_id": nonfiction.id},
        {"name": "Healthy Cooking Cookbook", "brand": "Wellness Books", "sku": "NFC-002", "price": Decimal("32.99"), "description": "200+ healthy recipes", "category_id": nonfiction.id},
        {"name": "Personal Development", "brand": "GrowthMind Publishing", "sku": "NFC-003", "price": Decimal("27.99"), "description": "Self-improvement guide", "category_id": nonfiction.id},

        # Books - Children's
        {"name": "Picture Book Collection", "brand": "KidStories", "sku": "CHD-001", "price": Decimal("44.99"), "description": "Set of 5 illustrated picture books", "category_id": childrens_books.id},
        {"name": "Young Adult Adventure", "brand": "Teen Reads", "sku": "CHD-002", "price": Decimal("19.99"), "description": "Exciting YA adventure novel", "category_id": childrens_books.id},

        # Sports - Fitness
        {"name": "Adjustable Dumbbells Set", "brand": "FitPro", "sku": "FIT-001", "price": Decimal("249.99"), "description": "5-50 lb adjustable dumbbell pair", "category_id": fitness.id},
        {"name": "Yoga Mat Premium", "brand": "YogaFlex", "sku": "FIT-002", "price": Decimal("49.99"), "description": "Non-slip yoga mat with carrying strap", "category_id": fitness.id},
        {"name": "Resistance Bands Set", "brand": "FlexFit", "sku": "FIT-003", "price": Decimal("29.99"), "description": "5 resistance levels workout bands", "category_id": fitness.id},
        {"name": "Foam Roller", "brand": "RecoverPro", "sku": "FIT-004", "price": Decimal("34.99"), "description": "High-density foam roller", "category_id": fitness.id},

        # Sports - Camping
        {"name": "4-Person Tent", "brand": "CampMaster", "sku": "CMP-001", "price": Decimal("199.99"), "description": "Weatherproof camping tent", "category_id": camping.id},
        {"name": "Sleeping Bag", "brand": "WarmSleep", "sku": "CMP-002", "price": Decimal("79.99"), "description": "3-season sleeping bag", "category_id": camping.id},
        {"name": "Camping Stove Portable", "brand": "CookOutdoors", "sku": "CMP-003", "price": Decimal("59.99"), "description": "Compact camping stove", "category_id": camping.id},

        # Sports - Cycling
        {"name": "Mountain Bike 29-inch", "brand": "TrailRide", "sku": "CYC-001", "price": Decimal("599.99"), "description": "Durable mountain bike", "category_id": cycling.id},
        {"name": "Bike Helmet", "brand": "SafeRide", "sku": "CYC-002", "price": Decimal("69.99"), "description": "Protective cycling helmet", "category_id": cycling.id},
        {"name": "Bike Lock Heavy-Duty", "brand": "SecureLock", "sku": "CYC-003", "price": Decimal("39.99"), "description": "U-lock with cable", "category_id": cycling.id},

        # Beauty - Skincare
        {"name": "Face Moisturizer SPF 30", "brand": "GlowSkin", "sku": "SKN-001", "price": Decimal("34.99"), "description": "Daily moisturizer with sun protection", "category_id": skincare.id},
        {"name": "Vitamin C Serum", "brand": "RadiantCare", "sku": "SKN-002", "price": Decimal("29.99"), "description": "Brightening vitamin C serum", "category_id": skincare.id},
        {"name": "Cleansing Face Wash", "brand": "PureClean", "sku": "SKN-003", "price": Decimal("19.99"), "description": "Gentle daily face wash", "category_id": skincare.id},

        # Beauty - Makeup
        {"name": "Makeup Brush Set", "brand": "BeautyTools", "sku": "MKP-001", "price": Decimal("49.99"), "description": "Professional 12-piece brush set", "category_id": makeup.id},
        {"name": "Foundation Long-Wear", "brand": "FlawlessFace", "sku": "MKP-002", "price": Decimal("39.99"), "description": "24-hour wear foundation", "category_id": makeup.id},
        {"name": "Eyeshadow Palette", "brand": "ColorPro", "sku": "MKP-003", "price": Decimal("44.99"), "description": "20-color eyeshadow palette", "category_id": makeup.id},

        # Beauty - Hair Care
        {"name": "Shampoo & Conditioner Set", "brand": "ShineHair", "sku": "HAR-001", "price": Decimal("29.99"), "description": "Sulfate-free hair care duo", "category_id": haircare.id},
        {"name": "Hair Dryer Ionic", "brand": "StylePro", "sku": "HAR-002", "price": Decimal("79.99"), "description": "Professional ionic hair dryer", "category_id": haircare.id},
        {"name": "Hair Straightener", "brand": "SleekStyle", "sku": "HAR-003", "price": Decimal("69.99"), "description": "Ceramic plate straightener", "category_id": haircare.id},

        # Toys - Action Figures
        {"name": "Superhero Action Figure", "brand": "HeroToys", "sku": "TOY-001", "price": Decimal("24.99"), "description": "Poseable superhero figure", "category_id": action_figures.id},
        {"name": "Robot Transformer", "brand": "RoboPlay", "sku": "TOY-002", "price": Decimal("34.99"), "description": "Transforming robot toy", "category_id": action_figures.id},

        # Toys - Board Games
        {"name": "Strategy Board Game", "brand": "GameNight", "sku": "BRD-001", "price": Decimal("44.99"), "description": "Family strategy game", "category_id": board_games.id},
        {"name": "Card Game Classic", "brand": "CardPlay", "sku": "BRD-002", "price": Decimal("19.99"), "description": "Classic card game set", "category_id": board_games.id},
        {"name": "Puzzle 1000 Pieces", "brand": "PuzzleMaster", "sku": "BRD-003", "price": Decimal("24.99"), "description": "Challenging jigsaw puzzle", "category_id": board_games.id},

        # Toys - Educational
        {"name": "STEM Building Kit", "brand": "LearnPlay", "sku": "EDU-001", "price": Decimal("59.99"), "description": "Engineering building set", "category_id": educational.id},
        {"name": "Science Experiment Kit", "brand": "ScienceKids", "sku": "EDU-002", "price": Decimal("39.99"), "description": "50+ science experiments", "category_id": educational.id},
        {"name": "Coding Robot", "brand": "TechKids", "sku": "EDU-003", "price": Decimal("89.99"), "description": "Programmable robot toy", "category_id": educational.id},

        # Automotive (keeping it at 100+ total)
        {"name": "Car Phone Mount", "brand": "DriveSafe", "sku": "AUT-001", "price": Decimal("19.99"), "description": "Magnetic phone mount", "category_id": automotive.id},
        {"name": "Car Vacuum Portable", "brand": "CleanCar", "sku": "AUT-002", "price": Decimal("49.99"), "description": "Cordless car vacuum", "category_id": automotive.id},
        {"name": "Dash Cam HD", "brand": "RoadWatch", "sku": "AUT-003", "price": Decimal("89.99"), "description": "1080p dash camera", "category_id": automotive.id},
        {"name": "Car Air Freshener Set", "brand": "FreshRide", "sku": "AUT-004", "price": Decimal("14.99"), "description": "Pack of 6 air fresheners", "category_id": automotive.id},
    ]

    products = [Product(**{**data, "is_active": True}) for data in products_data]
    db.add_all(products)
    db.commit()
    print(f"  Created {len(products)} products")

    # === Seed Inventory ===
    print("Seeding inventory...")
    inventory_records = []
    for idx, product in enumerate(products):
        # Alternate between warehouses
        warehouse = warehouse_east if idx % 2 == 0 else warehouse_west
        # Vary quantities - some low stock, some high stock
        if idx % 7 == 0:
            quantity = 5  # Low stock
        elif idx % 11 == 0:
            quantity = 8  # Near reorder level
        else:
            quantity = 50 + (idx * 3) % 150  # Good stock

        inventory = Inventory(
            product_id=product.id,
            warehouse_id=warehouse.id,
            quantity=quantity,
            reorder_level=10
        )
        inventory_records.append(inventory)

    db.add_all(inventory_records)
    db.commit()
    print(f"  Created {len(inventory_records)} inventory records")

    # === Seed Discounts ===
    print("Seeding discounts...")
    now = datetime.utcnow()
    discounts_data = [
        {
            "code": "WELCOME10",
            "discount_type": "percentage",
            "discount_value": Decimal("10.00"),
            "min_order_amount": Decimal("50.00"),
            "valid_from": now - timedelta(days=30),
            "valid_to": now + timedelta(days=60),
            "max_uses": 1000,
            "times_used": 45,
            "is_active": True
        },
        {
            "code": "SAVE20",
            "discount_type": "percentage",
            "discount_value": Decimal("20.00"),
            "min_order_amount": Decimal("100.00"),
            "valid_from": now - timedelta(days=7),
            "valid_to": now + timedelta(days=30),
            "max_uses": 500,
            "times_used": 123,
            "is_active": True
        },
        {
            "code": "FREESHIP",
            "discount_type": "fixed_amount",
            "discount_value": Decimal("15.00"),
            "min_order_amount": Decimal("75.00"),
            "valid_from": now,
            "valid_to": now + timedelta(days=45),
            "max_uses": 250,
            "times_used": 12,
            "is_active": True
        },
        {
            "code": "EXPIRED",
            "discount_type": "percentage",
            "discount_value": Decimal("25.00"),
            "min_order_amount": Decimal("100.00"),
            "valid_from": now - timedelta(days=90),
            "valid_to": now - timedelta(days=30),
            "max_uses": 100,
            "times_used": 87,
            "is_active": False
        },
    ]

    discounts = [Discount(**data) for data in discounts_data]
    db.add_all(discounts)
    db.commit()
    print(f"  Created {len(discounts)} discounts")

    # === Seed Reviews ===
    print("Seeding reviews...")
    customer = db.query(Customer).filter(Customer.email == "customer@example.com").first()

    # Add reviews for first 20 products
    reviews_data = [
        {"product_id": products[0].id, "customer_id": customer.id, "rating": 5, "review_text": "Amazing laptop! Super fast and great build quality.", "helpful_count": 15, "is_hidden": False},
        {"product_id": products[0].id, "customer_id": customer.id, "rating": 4, "review_text": "Good laptop but battery life could be better.", "helpful_count": 8, "is_hidden": False},
        {"product_id": products[1].id, "customer_id": customer.id, "rating": 5, "review_text": "Perfect for business travel. Lightweight and powerful.", "helpful_count": 12, "is_hidden": False},
        {"product_id": products[2].id, "customer_id": customer.id, "rating": 5, "review_text": "Best gaming laptop I've owned. Runs all games smoothly.", "helpful_count": 23, "is_hidden": False},
        {"product_id": products[5].id, "customer_id": customer.id, "rating": 5, "review_text": "This phone is incredible! Camera quality is outstanding.", "helpful_count": 31, "is_hidden": False},
        {"product_id": products[5].id, "customer_id": customer.id, "rating": 3, "review_text": "Good phone but expensive for what you get.", "helpful_count": 5, "is_hidden": False},
        {"product_id": products[8].id, "customer_id": customer.id, "rating": 5, "review_text": "Best noise cancellation I've experienced.", "helpful_count": 19, "is_hidden": False},
        {"product_id": products[8].id, "customer_id": customer.id, "rating": 4, "review_text": "Great sound quality, comfortable to wear.", "helpful_count": 11, "is_hidden": False},
        {"product_id": products[15].id, "customer_id": customer.id, "rating": 5, "review_text": "Love this console! Graphics are amazing.", "helpful_count": 42, "is_hidden": False},
        {"product_id": products[20].id, "customer_id": customer.id, "rating": 4, "review_text": "Comfortable t-shirt, washes well.", "helpful_count": 6, "is_hidden": False},
        {"product_id": products[30].id, "customer_id": customer.id, "rating": 5, "review_text": "Very comfortable running shoes!", "helpful_count": 14, "is_hidden": False},
        {"product_id": products[35].id, "customer_id": customer.id, "rating": 5, "review_text": "Best office chair I've owned. My back thanks me.", "helpful_count": 27, "is_hidden": False},
        {"product_id": products[38].id, "customer_id": customer.id, "rating": 4, "review_text": "Makes great coffee every morning.", "helpful_count": 9, "is_hidden": False},
        {"product_id": products[60].id, "customer_id": customer.id, "rating": 5, "review_text": "Dumbbells are sturdy and easy to adjust.", "helpful_count": 18, "is_hidden": False},
        {"product_id": products[61].id, "customer_id": customer.id, "rating": 5, "review_text": "Perfect yoga mat, great grip.", "helpful_count": 13, "is_hidden": False},
    ]

    reviews = [Review(**data) for data in reviews_data]
    db.add_all(reviews)
    db.commit()
    print(f"  Created {len(reviews)} reviews")

    print("\n✅ Database seeding completed successfully!")
    print("\n=== Default Credentials ===")
    print("  Admin:            admin@example.com / Admin123!")
    print("  Customer:         customer@example.com / Customer123!")
    print("  Inventory Mgr:    inventory@example.com / Inventory123!")
    print("  Customer Support: support@example.com / Support123!")


def main():
    """Main entry point for seed script."""
    # Initialize database
    init_db()

    # Create session and seed
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
