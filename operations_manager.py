"""
Operations Manager module for the Library Management System CLI.

Provides user interface and menu-driven operations for the library system.
Demonstrates proper separation of concerns (UI logic vs business logic).
"""

from library import Library
from fine_manager import FineManager
from exceptions import *
from datetime import datetime


class OperationsManager:
    """
    Manages CLI operations for the library system.
    
    Handles user input, menu navigation, and delegates to Library class
    for actual business logic. Demonstrates separation of concerns.
    """

    def __init__(self) -> None:
        """Initialize the operations manager with a Library instance."""
        self.library = Library()

    @staticmethod
    def _get_valid_input(prompt: str, input_type=str, allow_empty: bool = False):
        """
        Get validated input from user.
        
        Args:
            prompt: Prompt to display.
            input_type: Expected type of input.
            allow_empty: Whether empty input is allowed.
            
        Returns:
            User input in the specified type.
        """
        while True:
            try:
                user_input = input(prompt).strip()

                if not user_input and allow_empty:
                    return user_input

                if not user_input and not allow_empty:
                    print("❌ Input cannot be empty. Please try again.")
                    continue

                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input

            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\n⚠️  Operation cancelled.")
                raise

    def display_menu(self) -> None:
        """Display main menu options."""
        print("\n" + "="*60)
        print("📚 LIBRARY MANAGEMENT SYSTEM".center(60))
        print("="*60)
        print("""
        1.  ➕ Add Book
        2.  👤 Add User
        3.  📖 Issue Book
        4.  🔄 Return Book
        5.  🔍 Search Books
        6.  📚 View All Books
        7.  👥 View All Users
        8.  📋 View Issued Books
        9.  ⏰ View Overdue Books
        10. 📊 View Library Statistics
        11. 💰 View Fine Summary
        12. ⚙️  Admin Options
        0.  ❌ Exit
        """)
        print("="*60)

    def display_admin_menu(self) -> None:
        """Display admin menu options."""
        print("\n" + "="*60)
        print("⚙️  ADMIN OPTIONS".center(60))
        print("="*60)
        print("""
        1. ❌ Remove Book
        2. 📜 View Transaction History
        3. 👤 Search User Details
        4. 📖 Search Book Details
        5. 🔙 Back to Main Menu
        """)
        print("="*60)

    def add_book(self) -> None:
        """Add a new book to the library."""
        print("\n" + "="*60)
        print("➕ ADD NEW BOOK".center(60))
        print("="*60)

        try:
            book_id = self._get_valid_input("Enter Book ID: ")
            title = self._get_valid_input("Enter Book Title: ")
            author = self._get_valid_input("Enter Book Author: ")
            isbn = self._get_valid_input(
                "Enter ISBN (optional, press Enter to skip): ",
                allow_empty=True
            )
            quantity = self._get_valid_input(
                "Enter Quantity: ", int
            )

            if quantity <= 0:
                print("❌ Quantity must be greater than 0.")
                return

            book = self.library.add_book(
                book_id, title, author,
                isbn if isbn else None,
                quantity
            )
            print(f"\n✅ Book added successfully!")
            print(f"   ID: {book.book_id}")
            print(f"   Title: {book.title}")
            print(f"   Author: {book.author}")
            print(f"   Quantity: {quantity}")

        except BookAlreadyExistsError as e:
            print(f"\n❌ {str(e)}")
        except InvalidBookDataError as e:
            print(f"\n❌ Invalid book data: {str(e)}")
        except Exception as e:
            print(f"\n❌ Error adding book: {str(e)}")

    def add_user(self) -> None:
        """Add a new user to the library."""
        print("\n" + "="*60)
        print("👤 ADD NEW USER".center(60))
        print("="*60)

        try:
            user_id = self._get_valid_input("Enter User ID: ")
            name = self._get_valid_input("Enter Full Name: ")
            email = self._get_valid_input(
                "Enter Email (optional, press Enter to skip): ",
                allow_empty=True
            )
            phone = self._get_valid_input(
                "Enter Phone (optional, press Enter to skip): ",
                allow_empty=True
            )

            user = self.library.add_user(
                user_id, name,
                email if email else None,
                phone if phone else None
            )
            print(f"\n✅ User created successfully!")
            print(f"   ID: {user.user_id}")
            print(f"   Name: {user.name}")

        except UserAlreadyExistsError as e:
            print(f"\n❌ {str(e)}")
        except InvalidUserDataError as e:
            print(f"\n❌ Invalid user data: {str(e)}")
        except Exception as e:
            print(f"\n❌ Error adding user: {str(e)}")

    def issue_book(self) -> None:
        """Issue a book to a user."""
        print("\n" + "="*60)
        print("📖 ISSUE BOOK".center(60))
        print("="*60)

        try:
            user_id = self._get_valid_input("Enter User ID: ")
            book_id = self._get_valid_input("Enter Book ID: ")
            days = self._get_valid_input(
                "Enter Issue Duration (days, default 14): ",
                int
            )

            if days <= 0:
                print("❌ Issue duration must be greater than 0.")
                return

            transaction = self.library.issue_book(user_id, book_id, days)
            user = self.library.get_user(user_id)
            book = self.library.get_book(book_id)

            print(f"\n✅ Book issued successfully!")
            print(f"   Transaction ID: {transaction.transaction_id}")
            print(f"   User: {user.name}")
            print(f"   Book: {book.title}")
            print(f"   Issue Date: {transaction.issue_date.strftime('%d-%m-%Y')}")
            print(f"   Due Date: {transaction.due_date.strftime('%d-%m-%Y')}")
            print(f"   Days: {days}")

        except UserNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except BookNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except InsufficientBookQuantityError as e:
            print(f"\n❌ {str(e)}")
        except Exception as e:
            print(f"\n❌ Error issuing book: {str(e)}")

    def return_book(self) -> None:
        """Return a book from a user."""
        print("\n" + "="*60)
        print("🔄 RETURN BOOK".center(60))
        print("="*60)

        try:
            user_id = self._get_valid_input("Enter User ID: ")
            book_id = self._get_valid_input("Enter Book ID: ")

            transaction = self.library.return_book(user_id, book_id)
            user = self.library.get_user(user_id)
            book = self.library.get_book(book_id)

            print(f"\n✅ Book returned successfully!")
            print(f"   User: {user.name}")
            print(f"   Book: {book.title}")
            print(f"   Return Date: {transaction.return_date.strftime('%d-%m-%Y')}")
            print(f"   Due Date: {transaction.due_date.strftime('%d-%m-%Y')}")

            if transaction.fine_amount > 0:
                print(f"   ⚠️  Fine Amount: {FineManager.format_fine_display(transaction.fine_amount)}")
                print(f"      Days Overdue: {transaction.get_days_overdue()}")
            else:
                print(f"   ✅ No fine (returned on time)")

        except UserNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except BookNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except BookNotIssuedError as e:
            print(f"\n❌ {str(e)}")
        except Exception as e:
            print(f"\n❌ Error returning book: {str(e)}")

    def search_books(self) -> None:
        """Search for books in the library."""
        print("\n" + "="*60)
        print("🔍 SEARCH BOOKS".center(60))
        print("="*60)

        query = self._get_valid_input("Enter search query (title or author): ")

        try:
            books = self.library.search_books(query)

            if not books:
                print(f"\n❌ No books found matching '{query}'")
                return

            print(f"\n📚 Found {len(books)} book(s):\n")
            for idx, book in enumerate(books, 1):
                print(f"{idx}. {book.title}")
                print(f"   Author: {book.author}")
                print(f"   ID: {book.book_id}")
                print(f"   Available: {book.available_quantity}/{book.total_quantity}")
                print()

        except Exception as e:
            print(f"\n❌ Error searching books: {str(e)}")

    def view_all_books(self) -> None:
        """Display all books in the library."""
        print("\n" + "="*60)
        print("📚 ALL BOOKS".center(60))
        print("="*60)

        try:
            books = self.library.get_all_books()

            if not books:
                print("\n❌ No books in the library")
                return

            print(f"\n📚 Total Books: {len(books)}\n")
            print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Available':<15}")
            print("-" * 75)

            for book in books:
                status = "✅" if book.available_quantity > 0 else "❌"
                print(
                    f"{book.book_id:<10} {book.title:<30} "
                    f"{book.author:<20} "
                    f"{status} {book.available_quantity}/{book.total_quantity}"
                )

        except Exception as e:
            print(f"\n❌ Error retrieving books: {str(e)}")

    def view_all_users(self) -> None:
        """Display all users in the library."""
        print("\n" + "="*60)
        print("👥 ALL USERS".center(60))
        print("="*60)

        try:
            users = self.library.get_all_users()

            if not users:
                print("\n❌ No users in the system")
                return

            print(f"\n👥 Total Users: {len(users)}\n")
            print(f"{'ID':<15} {'Name':<25} {'Email':<30} {'Phone':<15}")
            print("-" * 85)

            for user in users:
                print(
                    f"{user.user_id:<15} {user.name:<25} "
                    f"{user.email or 'N/A':<30} {user.phone or 'N/A':<15}"
                )

        except Exception as e:
            print(f"\n❌ Error retrieving users: {str(e)}")

    def view_issued_books(self) -> None:
        """View books issued to a specific user."""
        print("\n" + "="*60)
        print("📋 ISSUED BOOKS".center(60))
        print("="*60)

        try:
            user_id = self._get_valid_input("Enter User ID: ")
            user = self.library.get_user(user_id)
            issued_books = self.library.get_user_issued_books(user_id)

            if not issued_books:
                print(f"\n✅ User '{user.name}' has no issued books")
                return

            print(f"\n📖 Books issued to {user.name}:\n")
            for idx, book_info in enumerate(issued_books, 1):
                due_date = datetime.fromisoformat(book_info["due_date"])
                issue_date = datetime.fromisoformat(book_info["issue_date"])

                print(f"{idx}. {book_info['title']}")
                print(f"   Author: {book_info['author']}")
                print(f"   Issue Date: {issue_date.strftime('%d-%m-%Y')}")
                print(f"   Due Date: {due_date.strftime('%d-%m-%Y')}")
                print(f"   Days Until Due: {book_info['days_until_due']}")

                if book_info["is_overdue"]:
                    print(f"   ⚠️  Status: OVERDUE")
                    print(f"   💰 Fine: {FineManager.format_fine_display(book_info['fine'])}")
                else:
                    print(f"   ✅ Status: On Time")
                print()

        except UserNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except Exception as e:
            print(f"\n❌ Error retrieving issued books: {str(e)}")

    def view_overdue_books(self) -> None:
        """View all overdue books in the system."""
        print("\n" + "="*60)
        print("⏰ OVERDUE BOOKS".center(60))
        print("="*60)

        try:
            overdue = self.library.get_overdue_books()

            if not overdue:
                print("\n✅ No overdue books in the system")
                return

            print(f"\n⏰ Total Overdue: {len(overdue)}\n")
            for idx, item in enumerate(overdue, 1):
                print(f"{idx}. {item['book_title']}")
                print(f"   User: {item['user_name']} ({item['user_id']})")
                print(f"   Due Date: {item['due_date']}")
                print(f"   Days Overdue: {item['days_overdue']}")
                print(f"   💰 Fine: {FineManager.format_fine_display(item['fine_amount'])}")
                print()

        except Exception as e:
            print(f"\n❌ Error retrieving overdue books: {str(e)}")

    def view_statistics(self) -> None:
        """Display library statistics."""
        print("\n" + "="*60)
        print("📊 LIBRARY STATISTICS".center(60))
        print("="*60)

        try:
            stats = self.library.get_library_statistics()

            print(f"""
    📚 Total Books in Library: {stats['total_books']}
       ✅ Available Books: {stats['available_books']}
       📖 Issued Books: {stats['issued_books']}

    👥 Total Registered Users: {stats['total_users']}

    📋 Transaction Statistics:
       🔄 Active Transactions: {stats['active_transactions']}
       ✔️  Completed Transactions: {stats['total_transactions'] - stats['active_transactions']}
       📊 Total Transactions: {stats['total_transactions']}

    💰 Fine Collection:
       Total Fine Collected: {FineManager.format_fine_display(stats['total_fine_collected'])}
            """)

        except Exception as e:
            print(f"\n❌ Error retrieving statistics: {str(e)}")

    def view_fine_summary(self) -> None:
        """View fine collection summary."""
        print("\n" + "="*60)
        print("💰 FINE SUMMARY".center(60))
        print("="*60)

        try:
            overdue = self.library.get_overdue_books()

            if not overdue:
                print("\n✅ No pending fines")
                total_fine = 0
            else:
                total_fine = sum(item['fine_amount'] for item in overdue)
                print(f"\n📊 Pending Fines:\n")
                for item in overdue:
                    print(f"  {item['user_name']}: {FineManager.format_fine_display(item['fine_amount'])}")

            print(f"\n{'='*60}")
            print(f"Total Pending Fine: {FineManager.format_fine_display(total_fine)}")
            print("="*60)

        except Exception as e:
            print(f"\n❌ Error retrieving fine summary: {str(e)}")

    def remove_book(self) -> None:
        """Remove a book from the library."""
        print("\n" + "="*60)
        print("❌ REMOVE BOOK".center(60))
        print("="*60)

        try:
            book_id = self._get_valid_input("Enter Book ID: ")
            book = self.library.get_book(book_id)

            if book.issued_quantity > 0:
                print(f"\n❌ Cannot remove '{book.title}'")
                print(f"   {book.issued_quantity} copies are still issued")
                return

            confirm = input(
                f"Are you sure you want to remove '{book.title}'? (yes/no): "
            ).lower()

            if confirm != "yes":
                print("\n⚠️  Operation cancelled")
                return

            self.library.remove_book(book_id)
            print(f"\n✅ Book removed successfully!")

        except BookNotFoundError as e:
            print(f"\n❌ {str(e)}")
        except InvalidBookDataError as e:
            print(f"\n❌ {str(e)}")
        except Exception as e:
            print(f"\n❌ Error removing book: {str(e)}")

    def view_transaction_history(self) -> None:
        """View transaction history."""
        print("\n" + "="*60)
        print("📜 TRANSACTION HISTORY".center(60))
        print("="*60)

        try:
            user_id = self._get_valid_input(
                "Enter User ID (optional, press Enter for all): ",
                allow_empty=True
            )

            history = self.library.get_transaction_history(
                user_id if user_id else None
            )

            if not history:
                print("\n❌ No transaction history found")
                return

            print(f"\n📜 Total Transactions: {len(history)}\n")
            for idx, trans in enumerate(history, 1):
                print(f"{idx}. User: {trans['user_id']}, Book: {trans['book_id']}")
                print(f"   Type: {trans['transaction_type']}")
                print(f"   Issue Date: {trans['issue_date']}")
                if trans['return_date']:
                    print(f"   Return Date: {trans['return_date']}")
                    print(f"   Fine: {FineManager.format_fine_display(trans['fine_amount'])}")
                print()

        except Exception as e:
            print(f"\n❌ Error retrieving history: {str(e)}")

    def search_user_details(self) -> None:
        """Search and display user details."""
        print("\n" + "="*60)
        print("👤 SEARCH USER".center(60))
        print("="*60)

        try:
            query = self._get_valid_input("Enter User ID or Name: ")
            users = self.library.search_users(query)

            if not users:
                print(f"\n❌ No users found matching '{query}'")
                return

            print(f"\n👤 Found {len(users)} user(s):\n")
            for user in users:
                issued = self.library.get_user_issued_books(user.user_id)
                print(f"ID: {user.user_id}")
                print(f"Name: {user.name}")
                print(f"Email: {user.email or 'N/A'}")
                print(f"Phone: {user.phone or 'N/A'}")
                print(f"Books Issued: {len(issued)}")
                print()

        except Exception as e:
            print(f"\n❌ Error searching users: {str(e)}")

    def search_book_details(self) -> None:
        """Search and display book details."""
        print("\n" + "="*60)
        print("📖 SEARCH BOOK".center(60))
        print("="*60)

        try:
            query = self._get_valid_input("Enter Book Title or Author: ")
            books = self.library.search_books(query)

            if not books:
                print(f"\n❌ No books found matching '{query}'")
                return

            print(f"\n📖 Found {len(books)} book(s):\n")
            for book in books:
                print(f"ID: {book.book_id}")
                print(f"Title: {book.title}")
                print(f"Author: {book.author}")
                print(f"ISBN: {book.isbn or 'N/A'}")
                print(f"Total Quantity: {book.total_quantity}")
                print(f"Available: {book.available_quantity}")
                print(f"Issued: {book.issued_quantity}")
                print()

        except Exception as e:
            print(f"\n❌ Error searching books: {str(e)}")

    def handle_admin_menu(self) -> None:
        """Handle admin menu operations."""
        while True:
            self.display_admin_menu()
            try:
                choice = self._get_valid_input("Enter your choice: ", int)

                if choice == 1:
                    self.remove_book()
                elif choice == 2:
                    self.view_transaction_history()
                elif choice == 3:
                    self.search_user_details()
                elif choice == 4:
                    self.search_book_details()
                elif choice == 5:
                    break
                else:
                    print("❌ Invalid choice. Please try again.")

            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                break

    def run(self) -> None:
        """Run the main application loop."""
        print("\n" + "="*60)
        print("Welcome to Library Management System!".center(60))
        print("="*60)

        while True:
            try:
                self.display_menu()
                choice = self._get_valid_input("Enter your choice: ", int)

                if choice == 1:
                    self.add_book()
                elif choice == 2:
                    self.add_user()
                elif choice == 3:
                    self.issue_book()
                elif choice == 4:
                    self.return_book()
                elif choice == 5:
                    self.search_books()
                elif choice == 6:
                    self.view_all_books()
                elif choice == 7:
                    self.view_all_users()
                elif choice == 8:
                    self.view_issued_books()
                elif choice == 9:
                    self.view_overdue_books()
                elif choice == 10:
                    self.view_statistics()
                elif choice == 11:
                    self.view_fine_summary()
                elif choice == 12:
                    self.handle_admin_menu()
                elif choice == 0:
                    print("\n" + "="*60)
                    print("Thank you for using Library Management System!".center(60))
                    print("="*60 + "\n")
                    break
                else:
                    print("❌ Invalid choice. Please select a valid option.")

            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Application interrupted by user.")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
