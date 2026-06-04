"""
Custom exceptions for Library Management System.

Provides specific exception classes for different error scenarios
to enable proper error handling and debugging.
"""


class LibraryException(Exception):
    """Base exception class for all library-related errors."""
    pass


class UserException(LibraryException):
    """Exception raised for user-related errors."""
    pass


class UserNotFoundError(UserException):
    """Raised when a user is not found in the system."""
    pass


class UserAlreadyExistsError(UserException):
    """Raised when trying to create a user that already exists."""
    pass


class InvalidUserDataError(UserException):
    """Raised when user data is invalid."""
    pass


class BookException(LibraryException):
    """Exception raised for book-related errors."""
    pass


class BookNotFoundError(BookException):
    """Raised when a book is not found in the system."""
    pass


class BookAlreadyExistsError(BookException):
    """Raised when trying to add a book that already exists."""
    pass


class InsufficientBookQuantityError(BookException):
    """Raised when attempting to issue a book with insufficient quantity."""
    pass


class InvalidBookDataError(BookException):
    """Raised when book data is invalid."""
    pass


class TransactionException(LibraryException):
    """Exception raised for transaction-related errors."""
    pass


class InvalidTransactionError(TransactionException):
    """Raised when transaction data is invalid."""
    pass


class BookNotIssuedError(TransactionException):
    """Raised when trying to return a book that wasn't issued to the user."""
    pass


class FineException(LibraryException):
    """Exception raised for fine calculation errors."""
    pass


class InvalidFineDataError(FineException):
    """Raised when fine data is invalid."""
    pass


class DatabaseException(LibraryException):
    """Exception raised for database-related errors."""
    pass
