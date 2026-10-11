"""Password hashing using bcrypt directly (not passlib)."""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt with cost factor 12.
    
    Args:
        password: Plain text password
    
    Returns:
        Bcrypt hashed password string
    """
    # Cost factor 12 as required by REQ-AUTH-001 and REQ-SEC-002
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against bcrypt hash.
    
    Args:
        plain_password: Plain text password to check
        hashed_password: Bcrypt hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
