"""Database exception hierarchy. Independent of HTTP exceptions."""


class DatabaseError(Exception):
    """Base class for all iptv-db errors."""


class NotFoundError(DatabaseError):
    """Entity not found in database."""


class ConstraintViolationError(DatabaseError):
    """Unique, FK, or check constraint violated."""


class ConnectionError(DatabaseError):
    """Cannot connect to database."""
