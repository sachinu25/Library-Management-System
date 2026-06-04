"""
Fine management module for calculating library fines.

Implements the fine calculation logic:
- First 7 days free after due date
- ₹5 per day after grace period
"""

from datetime import datetime, timedelta
from typing import Tuple
from exceptions import InvalidFineDataError


class FineManager:
    """
    Manages fine calculations for overdue books.
    
    Implements the fine policy:
    - First 7 days: Free (grace period)
    - After 7 days: ₹5 per day
    """

    # Fine configuration constants
    GRACE_PERIOD_DAYS = 7  # Free days after due date
    FINE_PER_DAY = 5  # Fine in rupees per day

    @staticmethod
    def calculate_fine(due_date: datetime, return_date: datetime = None) -> Tuple[float, int]:
        """
        Calculate fine for overdue book.
        
        Args:
            due_date: The due date of the book.
            return_date: Date when book was returned (defaults to today).
            
        Returns:
            Tuple containing (fine_amount, days_overdue).
            
        Raises:
            InvalidFineDataError: If dates are invalid.
        """
        if not isinstance(due_date, datetime):
            raise InvalidFineDataError("Due date must be a datetime object")

        # Use current date if return date not provided
        if return_date is None:
            return_date = datetime.now()
        elif not isinstance(return_date, datetime):
            raise InvalidFineDataError("Return date must be a datetime object")

        # Calculate days difference
        days_difference = (return_date.date() - due_date.date()).days

        # If returned on time or early, no fine
        if days_difference <= 0:
            return 0.0, 0

        # Apply grace period
        days_overdue = days_difference - FineManager.GRACE_PERIOD_DAYS

        # If within grace period, no fine
        if days_overdue <= 0:
            return 0.0, days_difference

        # Calculate fine
        fine_amount = days_overdue * FineManager.FINE_PER_DAY

        return fine_amount, days_difference

    @staticmethod
    def is_overdue(due_date: datetime, check_date: datetime = None) -> bool:
        """
        Check if a due date is overdue.
        
        Args:
            due_date: The due date to check.
            check_date: Date to check against (defaults to today).
            
        Returns:
            True if overdue, False otherwise.
            
        Raises:
            InvalidFineDataError: If dates are invalid.
        """
        if not isinstance(due_date, datetime):
            raise InvalidFineDataError("Due date must be a datetime object")

        if check_date is None:
            check_date = datetime.now()
        elif not isinstance(check_date, datetime):
            raise InvalidFineDataError("Check date must be a datetime object")

        return check_date.date() > due_date.date()

    @staticmethod
    def get_days_until_due(due_date: datetime) -> int:
        """
        Get days remaining until due date.
        
        Args:
            due_date: The due date.
            
        Returns:
            Days remaining (negative if overdue).
            
        Raises:
            InvalidFineDataError: If date is invalid.
        """
        if not isinstance(due_date, datetime):
            raise InvalidFineDataError("Due date must be a datetime object")

        days = (due_date.date() - datetime.now().date()).days
        return days

    @staticmethod
    def get_grace_period_end_date(due_date: datetime) -> datetime:
        """
        Get the end date of grace period.
        
        Args:
            due_date: The original due date.
            
        Returns:
            datetime: End of grace period.
            
        Raises:
            InvalidFineDataError: If date is invalid.
        """
        if not isinstance(due_date, datetime):
            raise InvalidFineDataError("Due date must be a datetime object")

        return due_date + timedelta(days=FineManager.GRACE_PERIOD_DAYS)

    @staticmethod
    def format_fine_display(fine_amount: float) -> str:
        """
        Format fine amount for display.
        
        Args:
            fine_amount: Fine amount in rupees.
            
        Returns:
            Formatted string representation.
        """
        return f"₹{fine_amount:.2f}"
