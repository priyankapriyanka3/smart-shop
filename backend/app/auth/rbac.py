"""Role-Based Access Control (RBAC) definitions and permission checking."""
from typing import Dict, List, Set


# ROLE_PERMISSIONS map: role name -> set of allowed permissions
# Permission format: "resource:action" (e.g., "products:create", "orders:read")
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "admin": {
        # Admin has full access to all resources
        "products:create", "products:read", "products:update", "products:delete",
        "categories:create", "categories:read", "categories:update", "categories:delete",
        "orders:create", "orders:read", "orders:update", "orders:delete",
        "inventory:create", "inventory:read", "inventory:update", "inventory:delete",
        "promotions:create", "promotions:read", "promotions:update", "promotions:delete",
        "reviews:read", "reviews:approve", "reviews:reject", "reviews:delete",
        "users:create", "users:read", "users:update", "users:delete",
        "warehouses:create", "warehouses:read", "warehouses:update", "warehouses:delete",
        "suppliers:create", "suppliers:read", "suppliers:update", "suppliers:delete",
        "audit:read",
        "dashboard:read",
    },
    "inventory_manager": {
        # Inventory managers can manage inventory, warehouses, suppliers, and view products
        "products:read",
        "categories:read",
        "inventory:create", "inventory:read", "inventory:update", "inventory:delete",
        "warehouses:create", "warehouses:read", "warehouses:update",
        "suppliers:create", "suppliers:read", "suppliers:update",
        "orders:read",  # Read-only access to orders for fulfillment context
    },
    "customer_support": {
        # Customer support can view and manage orders, view customers, manage reviews
        "orders:read", "orders:update",
        "users:read",
        "products:read",
        "categories:read",
        "reviews:read", "reviews:approve", "reviews:reject",
        "promotions:read",
    },
    "customer": {
        # Regular customers can view catalog, manage their own cart/orders/reviews
        "products:read",
        "categories:read",
        "cart:create", "cart:read", "cart:update", "cart:delete",
        "orders:create", "orders:read",  # Can only read their own orders (enforced in route logic)
        "reviews:create", "reviews:read",  # Can create/read reviews
        "profile:read", "profile:update",  # Manage own profile
        "addresses:create", "addresses:read", "addresses:update", "addresses:delete",
    },
}


def check_permission(role_name: str, resource: str, action: str) -> bool:
    """
    Check if a role has permission for a resource:action.
    
    Args:
        role_name: Role name (e.g., "admin", "customer")
        resource: Resource name (e.g., "products", "orders")
        action: Action name (e.g., "read", "create", "update", "delete")
    
    Returns:
        True if role has permission, False otherwise
    """
    if role_name not in ROLE_PERMISSIONS:
        return False
    
    permission = f"{resource}:{action}"
    return permission in ROLE_PERMISSIONS[role_name]


def get_user_permissions(role_names: List[str]) -> Set[str]:
    """
    Get combined permissions for a list of roles.
    
    Args:
        role_names: List of role names
    
    Returns:
        Set of all permissions across roles
    """
    permissions = set()
    for role_name in role_names:
        if role_name in ROLE_PERMISSIONS:
            permissions.update(ROLE_PERMISSIONS[role_name])
    return permissions
