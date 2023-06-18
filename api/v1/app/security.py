from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed(password: str):
    """
    Hashes the provided password using the bcrypt hashing algorithm.

    Args:
        password: The password to hash.

    Returns:
        str: The hashed password.

    """
    return pwd_context.hash(password)


def verify(attempted_password, usr_password):
    """
    Verifies if the attempted password matches the hashed user password.

    Args:
        attempted_password: The attempted password.
        usr_password: The hashed user password.

    Returns:
        bool: True if the passwords match, False otherwise.

    """
    return pwd_context.verify(usr_password, attempted_password)

