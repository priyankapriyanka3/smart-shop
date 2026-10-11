"""Authentication and authorization module."""
from app.auth.jwt import create_access_token, decode_access_token
from app.auth.password import hash_password, verify_password
from app.auth.dependencies import get_current_user, require_auth, require_role
from app.auth.rbac import ROLE_PERMISSIONS, check_permission


__all__ = [
    "create_access_token",
    "decode_access_token",
    "hash_password",
    "verify_password",
    "get_current_user",
    "require_auth",
    "require_role",
    "ROLE_PERMISSIONS",
    "check_permission",
]
