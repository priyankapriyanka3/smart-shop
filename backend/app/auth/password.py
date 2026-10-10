"""
Password hashing utilities using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor >= 12.

    Args:
        password: Plain text password

    Returns:
        Hashed password as string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its bcrypt hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hashed password

    Returns:
        True if password matches hash, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
