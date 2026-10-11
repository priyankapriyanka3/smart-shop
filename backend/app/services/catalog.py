"""Catalog domain service: Product browsing, search, filtering."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.catalog import Category, Product
from app.models.inventory import Inventory
from app.schemas.catalog import (
    CategoryCreate,
    CategoryResponse,
    CategoryListResponse,
    ProductCreate,
    ProductResponse,
    ProductListResponse,
)


class CatalogService:
    """Service for catalog operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_categories(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> CategoryListResponse:
        """Get paginated list of categories."""
        query = self.db.query(Category)

        if status:
            query = query.filter(Category.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        categories = query.offset(offset).limit(page_size).all()

        return CategoryListResponse(
            items=[CategoryResponse.model_validate(cat) for cat in categories],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_category_by_id(self, category_id: int) -> Optional[CategoryResponse]:
        """Get category by ID."""
        category = self.db.query(Category).filter(Category.id == category_id).first()
        return CategoryResponse.model_validate(category) if category else None

    def get_category_by_slug(self, slug: str) -> Optional[CategoryResponse]:
        """Get category by slug."""
        category = self.db.query(Category).filter(Category.slug == slug).first()
        return CategoryResponse.model_validate(category) if category else None

    def create_category(self, data: CategoryCreate) -> CategoryResponse:
        """Create a new category."""
        category = Category(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return CategoryResponse.model_validate(category)

    def search_products(
        self,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        sort_by: str = "relevance",
        page: int = 1,
        page_size: int = 20,
    ) -> ProductListResponse:
        """Search and filter products."""
        db_query = self.db.query(Product).filter(Product.status == "active")

        # Search by keyword
        if query:
            search_filter = or_(
                Product.name.ilike(f"%{query}%"),
                Product.brand.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.sku.ilike(f"%{query}%"),
            )
            db_query = db_query.filter(search_filter)

        # Filter by category
        if category_id:
            db_query = db_query.filter(Product.category_id == category_id)

        # Filter by price range
        if min_price is not None:
            db_query = db_query.filter(Product.price >= min_price)
        if max_price is not None:
            db_query = db_query.filter(Product.price <= max_price)

        # Filter by brand
        if brand:
            db_query = db_query.filter(Product.brand == brand)

        # Sorting
        if sort_by == "price_asc":
            db_query = db_query.order_by(Product.price.asc())
        elif sort_by == "price_desc":
            db_query = db_query.order_by(Product.price.desc())
        elif sort_by == "newest":
            db_query = db_query.order_by(Product.created_at.desc())
        else:  # relevance (default)
            db_query = db_query.order_by(Product.name.asc())

        total = db_query.count()
        offset = (page - 1) * page_size
        products = db_query.offset(offset).limit(page_size).all()

        # Enrich with availability
        items = []
        for product in products:
            product_data = ProductResponse.model_validate(product)
            # Calculate available quantity from inventory
            available = (
                self.db.query(func.sum(Inventory.quantity))
                .filter(Inventory.product_id == product.id)
                .scalar()
                or 0
            )
            product_data.available_quantity = available
            items.append(product_data)

        return ProductListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_product_by_id(self, product_id: int) -> Optional[ProductResponse]:
        """Get product by ID with availability."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        product_data = ProductResponse.model_validate(product)
        # Calculate available quantity
        available = (
            self.db.query(func.sum(Inventory.quantity))
            .filter(Inventory.product_id == product.id)
            .scalar()
            or 0
        )
        product_data.available_quantity = available
        return product_data

    def get_product_by_slug(self, slug: str) -> Optional[ProductResponse]:
        """Get product by slug with availability."""
        product = self.db.query(Product).filter(Product.slug == slug).first()
        if not product:
            return None

        product_data = ProductResponse.model_validate(product)
        # Calculate available quantity
        available = (
            self.db.query(func.sum(Inventory.quantity))
            .filter(Inventory.product_id == product.id)
            .scalar()
            or 0
        )
        product_data.available_quantity = available
        return product_data

    def create_product(self, data: ProductCreate) -> ProductResponse:
        """Create a new product."""
        product = Product(**data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return ProductResponse.model_validate(product)

    def update_product_status(self, product_id: int, status: str) -> Optional[ProductResponse]:
        """Update product status."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        product.status = status
        self.db.commit()
        self.db.refresh(product)
        return ProductResponse.model_validate(product)
