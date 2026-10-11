"""Product service for business logic."""

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.category import CategoryList
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Service for product operations."""

    def __init__(self, db: Session):
        """Initialize product service."""
        self.db = db

    def _compute_stock_status(self, product: Product) -> str | None:
        """Compute stock status based on inventory."""
        total_quantity = (
            self.db.query(func.sum(Inventory.quantity))
            .filter(Inventory.product_id == product.id)
            .scalar()
        )

        if total_quantity is None or total_quantity == 0:
            return "out_of_stock"

        reorder_level = (
            self.db.query(Inventory.reorder_level)
            .filter(Inventory.product_id == product.id)
            .first()
        )

        if reorder_level and total_quantity <= reorder_level[0]:
            return "low_stock"

        return "in_stock"

    def get_products(
        self,
        page: int = 1,
        per_page: int = 20,
        category_id: int | None = None,
        is_active: str | None = None,
    ) -> tuple[list[Product], int]:
        """Get paginated products list."""
        query = self.db.query(Product)

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if is_active:
            # Filter by active status string
            query = query.filter(Product.is_active == is_active)

        total = query.count()

        products = (
            query
            .order_by(Product.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return products, total

    def get_product_by_id(self, product_id: int) -> Product | None:
        """Get product by ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create new product."""
        # Verify category exists
        category = self.db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise ValueError("Category not found")

        product = Product(
            name=product_data.name,
            description=product_data.description,
            brand=product_data.brand,
            sku=product_data.sku,
            price=product_data.price,
            category_id=product_data.category_id,
            is_active="draft",  # Default to draft
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        """Update product."""
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)

        return product

    def activate_product(self, product_id: int) -> Product | None:
        """Activate product."""
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        # Verify all required fields are populated
        if not all([product.name, product.brand, product.sku, product.price, product.category_id]):
            raise ValueError("Cannot activate product with missing required fields")

        product.is_active = "active"
        self.db.commit()
        self.db.refresh(product)

        return product

    def deactivate_product(self, product_id: int) -> Product | None:
        """Deactivate product."""
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        product.is_active = "inactive"
        self.db.commit()
        self.db.refresh(product)

        return product

    def search_products(
        self,
        query: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        brand: str | None = None,
        min_rating: float | None = None,
        in_stock: bool | None = None,
        sort_by: str = "relevance",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Product], int]:
        """Search products with filters and sorting."""
        db_query = self.db.query(Product).filter(Product.is_active == "active")

        # Text search
        if query:
            search_filter = or_(
                Product.name.ilike(f"%{query}%"),
                Product.brand.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
            )
            db_query = db_query.filter(search_filter)

        # Category filter
        if category_id:
            db_query = db_query.filter(Product.category_id == category_id)

        # Price range filter
        if min_price is not None:
            db_query = db_query.filter(Product.price >= min_price)
        if max_price is not None:
            db_query = db_query.filter(Product.price <= max_price)

        # Brand filter
        if brand:
            db_query = db_query.filter(Product.brand == brand)

        # Stock filter
        if in_stock:
            db_query = db_query.join(Inventory).filter(Inventory.quantity > 0)

        # Sorting
        if sort_by == "price_asc":
            db_query = db_query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            db_query = db_query.order_by(Product.price.desc())
        elif sort_by == "newest":
            db_query = db_query.order_by(Product.created_at.desc())
        else:  # relevance (default)
            db_query = db_query.order_by(Product.created_at.desc())

        total = db_query.count()

        products = (
            db_query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return products, total

    def get_categories(self) -> list[Category]:
        """Get all categories."""
        return self.db.query(Category).filter(Category.is_active.is_(True)).all()

    def get_category_hierarchy(self) -> list[CategoryList]:
        """Get categories in hierarchical structure."""
        # Get all active categories
        categories = self.db.query(Category).filter(Category.is_active.is_(True)).all()

        # Build hierarchy
        root_categories = []
        for cat in categories:
            if cat.parent_id is None:
                cat_dict = CategoryList.model_validate(cat)
                root_categories.append(cat_dict)

        # Add subcategories
        def add_subcategories(parent: CategoryList):
            for cat in categories:
                if cat.parent_id == parent.id:
                    child = CategoryList.model_validate(cat)
                    parent.subcategories.append(child)
                    add_subcategories(child)

        for root in root_categories:
            add_subcategories(root)

        return root_categories

    def get_category_by_id(self, category_id: int) -> Category | None:
        """Get category by ID."""
        return self.db.query(Category).filter(Category.id == category_id).first()
