"""
Database module for Library Management System.

This module handles all SQLite database operations including initialization,
connection management, and schema creation.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class DatabaseManager:
    """
    Manages SQLite database operations for the library system.
    
    Handles connection pooling, schema initialization, and provides
    context manager support for safe database operations.
    """

    def __init__(self, db_name: str = "library_system.db") -> None:
        """
        Initialize the database manager.
        
        Args:
            db_name: Name of the SQLite database file.
        """
        self.db_name = db_name
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection with row factory enabled.
        
        Returns:
            sqlite3.Connection: Database connection object.
        """
        try:
            connection = sqlite3.connect(self.db_name)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database: {str(e)}")

    @contextmanager
    def get_db_context(self):
        """
        Context manager for database operations.
        
        Yields:
            sqlite3.Connection: Database connection.
            
        Raises:
            DatabaseError: If database operation fails.
        """
        connection = self._get_connection()
        try:
            yield connection
            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            connection.close()

    def _initialize_database(self) -> None:
        """Initialize database schema if not already present."""
        with self.get_db_context() as conn:
            cursor = conn.cursor()
            self._create_tables(cursor)

    def _create_tables(self, cursor: sqlite3.Cursor) -> None:
        """
        Create database tables if they don't exist.
        
        Args:
            cursor: SQLite cursor object.
        """
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                isbn TEXT UNIQUE,
                total_quantity INTEGER NOT NULL,
                available_quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                book_id TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                issue_date TIMESTAMP,
                due_date TIMESTAMP,
                return_date TIMESTAMP,
                fine_amount REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            )
        """)

        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user 
            ON transactions (user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_book 
            ON transactions (book_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_status 
            ON transactions (status)
        """)

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL query string.
            params: Query parameters.
            
        Returns:
            List of dictionaries containing query results.
        """
        with self.get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string.
            params: Query parameters.
            
        Returns:
            Number of rows affected.
        """
        with self.get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query and return the row ID.
        
        Args:
            query: SQL query string.
            params: Query parameters.
            
        Returns:
            ID of the inserted row.
        """
        with self.get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
