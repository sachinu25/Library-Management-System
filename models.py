"""
Models module containing base classes and entity models.

Demonstrates proper OOP concepts including:
- Abstraction (ABC)
- Inheritance
- Encapsulation
- Polymorphism
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Any
from exceptions import *


class Entity(ABC):
    """
    Abstract base class for all entities in the library system.
    
    Defines common interface for all entity types to follow.
    Demonstrates abstraction and encapsulation principles.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entity to dictionary representation.
        
        Returns:
            Dictionary containing entity data.
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate entity data.
        
        Returns:
            True if valid, False otherwise.
        """
        pass

    @abstractmethod
    def get_id(self) -> str:
        """
        Get unique identifier for the entity.
        
        Returns:
            Unique identifier string.
        """
        pass


class User(Entity):
    """
    Represents a library user/patron.
    
    Demonstrates encapsulation through private attributes
    and inheritance from Entity.
    """

    def __init__(
        self,
        user_id: str,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> None:
        """
        Initialize a User object.
        
        Args:
            user_id: Unique user identifier.
            name: User's full name.
            email: User's email address.
            phone: User's phone number.
            
        Raises:
            InvalidUserDataError: If provided data is invalid.
        """
        self._user_id = user_id
        self._name = name
        self._email = email
        self._phone = phone
        self._created_at = datetime.now()
        
        if not self.validate():
            raise InvalidUserDataError("Invalid user data provided")

    @property
    def user_id(self) -> str:
        """Get user ID (read-only)."""
        return self._user_id

    @property
    def name(self) -> str:
        """Get user name (read-only)."""
        return self._name

    @property
    def email(self) -> Optional[str]:
        """Get user email (read-only)."""
        return self._email

    @property
    def phone(self) -> Optional[str]:
        """Get user phone (read-only)."""
        return self._phone

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp (read-only)."""
        return self._created_at

    def validate(self) -> bool:
        """
        Validate user data.
        
        Returns:
            True if user_id and name are non-empty strings.
        """
        if not isinstance(self._user_id, str) or not self._user_id.strip():
            return False
        if not isinstance(self._name, str) or not self._name.strip():
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user to dictionary.
        
        Returns:
            Dictionary representation of user.
        """
        return {
            "user_id": self._user_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "created_at": self._created_at.isoformat()
        }

    def get_id(self) -> str:
        """
        Get unique identifier.
        
        Returns:
            User ID.
        """
        return self._user_id

    def __repr__(self) -> str:
        """String representation of user."""
        return f"User(id={self._user_id}, name={self._name})"


class Book(Entity):
    """
    Represents a library book.
    
    Tracks book details and quantity management.
    Demonstrates encapsulation and inheritance principles.
    """

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        isbn: Optional[str] = None,
        total_quantity: int = 1
    ) -> None:
        """
        Initialize a Book object.
        
        Args:
            book_id: Unique book identifier.
            title: Book title.
            author: Book author.
            isbn: ISBN number (optional).
            total_quantity: Total copies available.
            
        Raises:
            InvalidBookDataError: If provided data is invalid.
        """
        self._book_id = book_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._total_quantity = total_quantity
        self._available_quantity = total_quantity
        self._created_at = datetime.now()
        
        if not self.validate():
            raise InvalidBookDataError("Invalid book data provided")

    @property
    def book_id(self) -> str:
        """Get book ID (read-only)."""
        return self._book_id

    @property
    def title(self) -> str:
        """Get book title (read-only)."""
        return self._title

    @property
    def author(self) -> str:
        """Get book author (read-only)."""
        return self._author

    @property
    def isbn(self) -> Optional[str]:
        """Get ISBN (read-only)."""
        return self._isbn

    @property
    def total_quantity(self) -> int:
        """Get total quantity (read-only)."""
        return self._total_quantity

    @property
    def available_quantity(self) -> int:
        """Get available quantity (read-only)."""
        return self._available_quantity

    @property
    def issued_quantity(self) -> int:
        """Get issued quantity."""
        return self._total_quantity - self._available_quantity

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp (read-only)."""
        return self._created_at

    def decrease_available_quantity(self, count: int = 1) -> None:
        """
        Decrease available quantity when book is issued.
        
        Args:
            count: Number of copies to decrease.
            
        Raises:
            InsufficientBookQuantityError: If quantity goes negative.
        """
        if self._available_quantity < count:
            raise InsufficientBookQuantityError(
                f"Insufficient quantity. Available: {self._available_quantity}"
            )
        self._available_quantity -= count

    def increase_available_quantity(self, count: int = 1) -> None:
        """
        Increase available quantity when book is returned.
        
        Args:
            count: Number of copies to increase.
            
        Raises:
            InvalidBookDataError: If quantity exceeds total.
        """
        if self._available_quantity + count > self._total_quantity:
            raise InvalidBookDataError(
                f"Cannot increase quantity beyond total ({self._total_quantity})"
            )
        self._available_quantity += count

    def validate(self) -> bool:
        """
        Validate book data.
        
        Returns:
            True if book_id, title, and author are valid.
        """
        if not isinstance(self._book_id, str) or not self._book_id.strip():
            return False
        if not isinstance(self._title, str) or not self._title.strip():
            return False
        if not isinstance(self._author, str) or not self._author.strip():
            return False
        if not isinstance(self._total_quantity, int) or self._total_quantity <= 0:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert book to dictionary.
        
        Returns:
            Dictionary representation of book.
        """
        return {
            "book_id": self._book_id,
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "total_quantity": self._total_quantity,
            "available_quantity": self._available_quantity,
            "issued_quantity": self.issued_quantity,
            "created_at": self._created_at.isoformat()
        }

    def get_id(self) -> str:
        """
        Get unique identifier.
        
        Returns:
            Book ID.
        """
        return self._book_id

    def __repr__(self) -> str:
        """String representation of book."""
        return (f"Book(id={self._book_id}, title={self._title}, "
                f"author={self._author}, available={self._available_quantity})")


class Transaction(Entity):
    """
    Represents a book transaction (issue/return).
    
    Tracks transaction history with dates and fine information.
    Demonstrates composition and encapsulation.
    """

    def __init__(
        self,
        transaction_id: int,
        user_id: str,
        book_id: str,
        issue_date: datetime,
        due_date: datetime,
        transaction_type: str = "ISSUE"
    ) -> None:
        """
        Initialize a Transaction object.
        
        Args:
            transaction_id: Unique transaction identifier.
            user_id: User who performed transaction.
            book_id: Book involved in transaction.
            issue_date: Date book was issued.
            due_date: Due date for return.
            transaction_type: Type of transaction (ISSUE/RETURN).
            
        Raises:
            InvalidTransactionError: If data is invalid.
        """
        self._transaction_id = transaction_id
        self._user_id = user_id
        self._book_id = book_id
        self._issue_date = issue_date
        self._due_date = due_date
        self._return_date: Optional[datetime] = None
        self._transaction_type = transaction_type
        self._fine_amount = 0.0
        self._status = "active"
        self._created_at = datetime.now()
        
        if not self.validate():
            raise InvalidTransactionError("Invalid transaction data")

    @property
    def transaction_id(self) -> int:
        """Get transaction ID (read-only)."""
        return self._transaction_id

    @property
    def user_id(self) -> str:
        """Get user ID (read-only)."""
        return self._user_id

    @property
    def book_id(self) -> str:
        """Get book ID (read-only)."""
        return self._book_id

    @property
    def issue_date(self) -> datetime:
        """Get issue date (read-only)."""
        return self._issue_date

    @property
    def due_date(self) -> datetime:
        """Get due date (read-only)."""
        return self._due_date

    @property
    def return_date(self) -> Optional[datetime]:
        """Get return date (read-only)."""
        return self._return_date

    @property
    def fine_amount(self) -> float:
        """Get fine amount (read-only)."""
        return self._fine_amount

    @property
    def status(self) -> str:
        """Get transaction status (read-only)."""
        return self._status

    def set_return_date(self, return_date: datetime) -> None:
        """
        Set the return date.
        
        Args:
            return_date: Date when book was returned.
        """
        self._return_date = return_date
        self._status = "completed"

    def set_fine_amount(self, fine_amount: float) -> None:
        """
        Set the fine amount.
        
        Args:
            fine_amount: Fine amount in rupees.
        """
        if fine_amount < 0:
            raise InvalidTransactionError("Fine amount cannot be negative")
        self._fine_amount = fine_amount

    def is_overdue(self) -> bool:
        """
        Check if transaction is overdue.
        
        Returns:
            True if current date is past due date and not returned.
        """
        if self._status == "completed":
            return False
        return datetime.now() > self._due_date

    def get_days_overdue(self) -> int:
        """
        Calculate days overdue.
        
        Returns:
            Number of days overdue (0 if not overdue or completed).
        """
        if self._status == "completed" or not self.is_overdue():
            return 0
        return (datetime.now() - self._due_date).days

    def validate(self) -> bool:
        """
        Validate transaction data.
        
        Returns:
            True if all required fields are valid.
        """
        if not isinstance(self._user_id, str) or not self._user_id.strip():
            return False
        if not isinstance(self._book_id, str) or not self._book_id.strip():
            return False
        if not isinstance(self._issue_date, datetime):
            return False
        if not isinstance(self._due_date, datetime):
            return False
        if self._issue_date >= self._due_date:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert transaction to dictionary.
        
        Returns:
            Dictionary representation of transaction.
        """
        return {
            "transaction_id": self._transaction_id,
            "user_id": self._user_id,
            "book_id": self._book_id,
            "issue_date": self._issue_date.isoformat(),
            "due_date": self._due_date.isoformat(),
            "return_date": self._return_date.isoformat() if self._return_date else None,
            "transaction_type": self._transaction_type,
            "fine_amount": self._fine_amount,
            "status": self._status,
            "days_overdue": self.get_days_overdue()
        }

    def get_id(self) -> str:
        """
        Get unique identifier.
        
        Returns:
            Transaction ID as string.
        """
        return str(self._transaction_id)

    def __repr__(self) -> str:
        """String representation of transaction."""
        return (f"Transaction(id={self._transaction_id}, user={self._user_id}, "
                f"book={self._book_id}, status={self._status})")
