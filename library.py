"""
Core library management module.

Implements the main Library class that handles all book and user operations
with database persistence. Demonstrates abstraction, encapsulation, and
polymorphism principles.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from database import DatabaseManager
from models import User, Book, Transaction
from fine_manager import FineManager
from exceptions import *


class Library:
    """
    Main library management system.
    
    Handles all book and user operations with SQLite persistence.
    Demonstrates proper OOP design with database integration.
    """

    # Default issue period in days
    DEFAULT_ISSUE_DAYS = 14

    def __init__(self, db_name: str = "library_system.db") -> None:
        """
        Initialize Library system.
        
        Args:
            db_name: Name of SQLite database file.
        """
        self.db = DatabaseManager(db_name)

    # ==================== USER OPERATIONS ====================

    def add_user(
        self,
        user_id: str,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> User:
        """
        Add a new user to the library system.
        
        Args:
            user_id: Unique user identifier.
            name: User's full name.
            email: User's email address.
            phone: User's phone number.
            
        Returns:
            Created User object.
            
        Raises:
            UserAlreadyExistsError: If user already exists.
            InvalidUserDataError: If user data is invalid.
        """
        # Check if user already exists
        existing = self.db.execute_query(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        if existing:
            raise UserAlreadyExistsError(f"User with ID {user_id} already exists")

        # Create user object (validates data)
        user = User(user_id, name, email, phone)

        # Insert into database
        self.db.execute_update(
            """INSERT INTO users (user_id, name, email, phone) 
               VALUES (?, ?, ?, ?)""",
            (user_id, name, email, phone)
        )

        return user

    def get_user(self, user_id: str) -> User:
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The user ID to search for.
            
        Returns:
            User object.
            
        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        result = self.db.execute_query(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        if not result:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        row = result[0]
        return User(row["user_id"], row["name"], row["email"], row["phone"])

    def search_users(self, name: str) -> List[User]:
        """
        Search users by name (case-insensitive, partial match).
        
        Args:
            name: Name to search for.
            
        Returns:
            List of matching User objects.
        """
        results = self.db.execute_query(
            "SELECT * FROM users WHERE LOWER(name) LIKE LOWER(?)",
            (f"%{name}%",)
        )

        return [
            User(row["user_id"], row["name"], row["email"], row["phone"])
            for row in results
        ]

    def get_all_users(self) -> List[User]:
        """
        Get all users in the system.
        
        Returns:
            List of all User objects.
        """
        results = self.db.execute_query("SELECT * FROM users ORDER BY name")
        return [
            User(row["user_id"], row["name"], row["email"], row["phone"])
            for row in results
        ]

    # ==================== BOOK OPERATIONS ====================

    def add_book(
        self,
        book_id: str,
        title: str,
        author: str,
        isbn: Optional[str] = None,
        total_quantity: int = 1
    ) -> Book:
        """
        Add a new book to the library.
        
        Args:
            book_id: Unique book identifier.
            title: Book title.
            author: Book author.
            isbn: ISBN number.
            total_quantity: Total copies to add.
            
        Returns:
            Created Book object.
            
        Raises:
            BookAlreadyExistsError: If book already exists.
            InvalidBookDataError: If book data is invalid.
        """
        # Check if book already exists
        existing = self.db.execute_query(
            "SELECT * FROM books WHERE book_id = ?", (book_id,)
        )
        if existing:
            raise BookAlreadyExistsError(f"Book with ID {book_id} already exists")

        # Create book object (validates data)
        book = Book(book_id, title, author, isbn, total_quantity)

        # Insert into database
        self.db.execute_update(
            """INSERT INTO books 
               (book_id, title, author, isbn, total_quantity, available_quantity) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (book_id, title, author, isbn, total_quantity, total_quantity)
        )

        return book

    def get_book(self, book_id: str) -> Book:
        """
        Retrieve a book by ID.
        
        Args:
            book_id: The book ID to search for.
            
        Returns:
            Book object.
            
        Raises:
            BookNotFoundError: If book doesn't exist.
        """
        result = self.db.execute_query(
            "SELECT * FROM books WHERE book_id = ?", (book_id,)
        )
        if not result:
            raise BookNotFoundError(f"Book with ID {book_id} not found")

        row = result[0]
        book = Book(
            row["book_id"], row["title"], row["author"],
            row["isbn"], row["total_quantity"]
        )
        # Manually set available quantity
        book._available_quantity = row["available_quantity"]
        return book

    def search_books(self, query: str) -> List[Book]:
        """
        Search books by title or author (case-insensitive, partial match).
        
        Args:
            query: Search query string.
            
        Returns:
            List of matching Book objects.
        """
        results = self.db.execute_query(
            """SELECT * FROM books 
               WHERE LOWER(title) LIKE LOWER(?) 
               OR LOWER(author) LIKE LOWER(?)
               ORDER BY title""",
            (f"%{query}%", f"%{query}%")
        )

        books = []
        for row in results:
            book = Book(
                row["book_id"], row["title"], row["author"],
                row["isbn"], row["total_quantity"]
            )
            book._available_quantity = row["available_quantity"]
            books.append(book)

        return books

    def get_all_books(self) -> List[Book]:
        """
        Get all books in the library.
        
        Returns:
            List of all Book objects.
        """
        results = self.db.execute_query(
            "SELECT * FROM books ORDER BY title"
        )

        books = []
        for row in results:
            book = Book(
                row["book_id"], row["title"], row["author"],
                row["isbn"], row["total_quantity"]
            )
            book._available_quantity = row["available_quantity"]
            books.append(book)

        return books

    def get_available_books(self) -> List[Book]:
        """
        Get books with available copies.
        
        Returns:
            List of Book objects with available_quantity > 0.
        """
        results = self.db.execute_query(
            "SELECT * FROM books WHERE available_quantity > 0 ORDER BY title"
        )

        books = []
        for row in results:
            book = Book(
                row["book_id"], row["title"], row["author"],
                row["isbn"], row["total_quantity"]
            )
            book._available_quantity = row["available_quantity"]
            books.append(book)

        return books

    def remove_book(self, book_id: str) -> None:
        """
        Remove a book from the library (if no copies issued).
        
        Args:
            book_id: Book ID to remove.
            
        Raises:
            BookNotFoundError: If book doesn't exist.
            InvalidBookDataError: If copies are still issued.
        """
        book = self.get_book(book_id)

        if book.issued_quantity > 0:
            raise InvalidBookDataError(
                f"Cannot remove book. {book.issued_quantity} copies still issued."
            )

        self.db.execute_update("DELETE FROM books WHERE book_id = ?", (book_id,))

    # ==================== TRANSACTION OPERATIONS ====================

    def issue_book(
        self,
        user_id: str,
        book_id: str,
        issue_days: int = DEFAULT_ISSUE_DAYS
    ) -> Transaction:
        """
        Issue a book to a user.
        
        Args:
            user_id: User ID.
            book_id: Book ID.
            issue_days: Number of days for issue (default 14).
            
        Returns:
            Created Transaction object.
            
        Raises:
            UserNotFoundError: If user doesn't exist.
            BookNotFoundError: If book doesn't exist.
            InsufficientBookQuantityError: If book not available.
        """
        # Verify user exists
        user = self.get_user(user_id)

        # Verify book exists and has copies
        book = self.get_book(book_id)
        if book.available_quantity <= 0:
            raise InsufficientBookQuantityError(
                f"No copies available for book: {book.title}"
            )

        # Create transaction
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=issue_days)

        self.db.execute_update(
            """UPDATE books SET available_quantity = available_quantity - 1 
               WHERE book_id = ?""",
            (book_id,)
        )

        transaction_id = self.db.execute_insert(
            """INSERT INTO transactions 
               (user_id, book_id, transaction_type, issue_date, due_date, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, book_id, "ISSUE", issue_date, due_date, "active")
        )

        transaction = Transaction(
            transaction_id, user_id, book_id, issue_date, due_date, "ISSUE"
        )
        return transaction

    def return_book(self, user_id: str, book_id: str) -> Transaction:
        """
        Return a book from a user.
        
        Args:
            user_id: User ID.
            book_id: Book ID.
            
        Returns:
            Updated Transaction object.
            
        Raises:
            UserNotFoundError: If user doesn't exist.
            BookNotFoundError: If book doesn't exist.
            BookNotIssuedError: If book wasn't issued to user.
        """
        # Verify user and book exist
        self.get_user(user_id)
        book = self.get_book(book_id)

        # Find active transaction
        result = self.db.execute_query(
            """SELECT * FROM transactions 
               WHERE user_id = ? AND book_id = ? AND status = 'active'
               ORDER BY issue_date DESC LIMIT 1""",
            (user_id, book_id)
        )

        if not result:
            raise BookNotIssuedError(
                f"Book {book.title} is not issued to user {user_id}"
            )

        transaction_row = result[0]
        return_date = datetime.now()

        # Calculate fine
        fine_amount, _ = FineManager.calculate_fine(
            datetime.fromisoformat(transaction_row["due_date"]), return_date
        )

        # Update transaction
        self.db.execute_update(
            """UPDATE transactions 
               SET return_date = ?, fine_amount = ?, status = 'completed'
               WHERE transaction_id = ?""",
            (return_date, fine_amount, transaction_row["transaction_id"])
        )

        # Update book quantity
        self.db.execute_update(
            """UPDATE books SET available_quantity = available_quantity + 1 
               WHERE book_id = ?""",
            (book_id,)
        )

        # Create transaction object
        transaction = Transaction(
            transaction_row["transaction_id"],
            user_id,
            book_id,
            datetime.fromisoformat(transaction_row["issue_date"]),
            datetime.fromisoformat(transaction_row["due_date"]),
            "RETURN"
        )
        transaction.set_return_date(return_date)
        transaction.set_fine_amount(fine_amount)

        return transaction

    def get_user_issued_books(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all books currently issued to a user.
        
        Args:
            user_id: User ID.
            
        Returns:
            List of dictionaries with book and transaction info.
            
        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        # Verify user exists
        self.get_user(user_id)

        results = self.db.execute_query(
            """SELECT t.transaction_id, b.title, b.author, t.issue_date, 
                      t.due_date, b.book_id
               FROM transactions t
               JOIN books b ON t.book_id = b.book_id
               WHERE t.user_id = ? AND t.status = 'active'
               ORDER BY t.issue_date DESC""",
            (user_id,)
        )

        issued_books = []
        for row in results:
            due_date = datetime.fromisoformat(row["due_date"])
            days_until_due = FineManager.get_days_until_due(due_date)
            is_overdue = days_until_due < 0

            issued_books.append({
                "transaction_id": row["transaction_id"],
                "title": row["title"],
                "author": row["author"],
                "book_id": row["book_id"],
                "issue_date": row["issue_date"],
                "due_date": row["due_date"],
                "days_until_due": days_until_due,
                "is_overdue": is_overdue,
                "fine": 0.0 if not is_overdue else FineManager.calculate_fine(due_date)[0]
            })

        return issued_books

    def get_transaction_history(
        self,
        user_id: Optional[str] = None,
        book_id: Optional[str] = None,
        status: str = "completed"
    ) -> List[Dict[str, Any]]:
        """
        Get transaction history with optional filtering.
        
        Args:
            user_id: Filter by user ID (optional).
            book_id: Filter by book ID (optional).
            status: Filter by status (default: completed).
            
        Returns:
            List of transaction dictionaries.
        """
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        if book_id:
            query += " AND book_id = ?"
            params.append(book_id)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY created_at DESC"

        results = self.db.execute_query(query, tuple(params))

        return [dict(row) for row in results]

    def get_overdue_books(self) -> List[Dict[str, Any]]:
        """
        Get all currently overdue books.
        
        Returns:
            List of dictionaries with user, book, and fine info.
        """
        results = self.db.execute_query(
            """SELECT t.transaction_id, u.user_id, u.name, b.title, b.author,
                      t.due_date, t.issue_date
               FROM transactions t
               JOIN users u ON t.user_id = u.user_id
               JOIN books b ON t.book_id = b.book_id
               WHERE t.status = 'active' AND t.due_date < datetime('now')
               ORDER BY t.due_date ASC"""
        )

        overdue_list = []
        for row in results:
            due_date = datetime.fromisoformat(row["due_date"])
            fine_amount, days_overdue = FineManager.calculate_fine(due_date)

            overdue_list.append({
                "transaction_id": row["transaction_id"],
                "user_id": row["user_id"],
                "user_name": row["name"],
                "book_title": row["title"],
                "book_author": row["author"],
                "due_date": row["due_date"],
                "days_overdue": days_overdue,
                "fine_amount": fine_amount
            })

        return overdue_list

    def get_library_statistics(self) -> Dict[str, Any]:
        """
        Get library statistics.
        
        Returns:
            Dictionary with various library statistics.
        """
        total_books = self.db.execute_query(
            "SELECT COUNT(*) as count FROM books"
        )[0]["count"]

        available_books = self.db.execute_query(
            "SELECT COUNT(*) as count FROM books WHERE available_quantity > 0"
        )[0]["count"]

        total_users = self.db.execute_query(
            "SELECT COUNT(*) as count FROM users"
        )[0]["count"]

        active_transactions = self.db.execute_query(
            "SELECT COUNT(*) as count FROM transactions WHERE status = 'active'"
        )[0]["count"]

        total_transactions = self.db.execute_query(
            "SELECT COUNT(*) as count FROM transactions"
        )[0]["count"]

        total_fine = self.db.execute_query(
            "SELECT COALESCE(SUM(fine_amount), 0) as total FROM transactions"
        )[0]["total"]

        return {
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": total_books - available_books,
            "total_users": total_users,
            "active_transactions": active_transactions,
            "total_transactions": total_transactions,
            "total_fine_collected": total_fine
        }
