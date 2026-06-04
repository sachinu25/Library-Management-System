# 📚 Library Management System

A professional-grade library management system built with Python, demonstrating advanced Object-Oriented Programming (OOP) principles and SQLite database integration.

## 🎯 Project Overview

This is a complete library management solution designed as a portfolio project for demonstrating:

- **Advanced OOP Concepts**: Inheritance, Encapsulation, Abstraction, Polymorphism
- **Database Management**: SQLite with proper schema design and relationships
- **Transaction Tracking**: Complete history of all library transactions
- **Fine Management**: Automated fine calculation with configurable policies
- **Clean Code**: PEP8 compliance, comprehensive docstrings, and modular architecture
- **Exception Handling**: Custom exceptions and proper error management

## ✨ Key Features

### User Management
- ✅ Add new library members (users)
- ✅ Search users by name or ID
- ✅ View user profile and issued books
- ✅ Track user transaction history

### Book Management
- ✅ Add books to the library inventory
- ✅ Remove books (with validation for issued copies)
- ✅ Search books by title or author
- ✅ View complete book catalog
- ✅ Track available and issued quantities

### Book Transactions
- ✅ Issue books to users with automatic due date calculation
- ✅ Return books with automatic fine calculation
- ✅ Configurable issue duration (default: 14 days)
- ✅ Complete transaction history with timestamps

### Fine Management
- ✅ Automatic fine calculation:
  - First 7 days after due date: Free (grace period)
  - After grace period: ₹5 per day
- ✅ View overdue books and pending fines
- ✅ Fine summary and collection tracking

### Reporting & Analytics
- ✅ Library statistics (total books, users, transactions)
- ✅ Overdue books report
- ✅ Transaction history with filtering
- ✅ Fine collection summary

## 🏗️ Architecture

### Modular Design

```
library_system/
├── database.py              # Database connection & schema management
├── models.py                # Entity classes with OOP principles
├── exceptions.py            # Custom exception definitions
├── fine_manager.py          # Fine calculation logic
├── library.py               # Core business logic
├── operations_manager.py    # CLI interface
├── main.py                  # Application entry point
├── library_system.db        # SQLite database (auto-created)
└── README.md               # Documentation
```

### Class Hierarchy

```
Entity (Abstract Base Class)
├── User
├── Book
└── Transaction

Database Management
└── DatabaseManager

Business Logic
└── Library

Fine Calculations
└── FineManager

User Interface
└── OperationsManager
```

## 💻 Technical Stack

- **Language**: Python 3.7+
- **Database**: SQLite3
- **Architecture**: Object-Oriented Programming (OOP)
- **Code Style**: PEP8 Compliant
- **Documentation**: Comprehensive Docstrings

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses built-in libraries only)

### Installation

1. Clone or download the project:
```bash
cd "Library System Project"
```

2. Verify all files are present:
```bash
ls -la  # or dir on Windows
```

Expected files:
- `database.py`
- `models.py`
- `exceptions.py`
- `fine_manager.py`
- `library.py`
- `operations_manager.py`
- `main.py`

### Running the Application

```bash
python main.py
```

The application will:
1. Create `library_system.db` if it doesn't exist
2. Initialize the database schema
3. Display the interactive menu

## 📖 Usage Guide

### Main Menu Options

```
1.  ➕ Add Book              - Add a new book to the library
2.  👤 Add User              - Register a new library member
3.  📖 Issue Book            - Issue a book to a user
4.  🔄 Return Book           - Return a book from a user
5.  🔍 Search Books          - Search books by title or author
6.  📚 View All Books        - Display all books in library
7.  👥 View All Users        - Display all registered users
8.  📋 View Issued Books     - View books issued to a user
9.  ⏰ View Overdue Books    - Display overdue books and fines
10. 📊 View Statistics       - View library statistics
11. 💰 View Fine Summary     - View fine collection details
12. ⚙️  Admin Options        - Access admin functions
0.  ❌ Exit                  - Exit the application
```

### Admin Options

```
1. ❌ Remove Book               - Remove a book from library
2. 📜 View Transaction History  - View complete transaction records
3. 👤 Search User Details       - Search and view user information
4. 📖 Search Book Details       - Search and view book information
5. 🔙 Back to Main Menu         - Return to main menu
```

### Example Workflows

#### Adding a Book
```
1. Select Option: 1 (Add Book)
2. Enter Book ID: B001
3. Enter Book Title: Python Programming
4. Enter Book Author: Guido van Rossum
5. Enter ISBN: 978-0134685991
6. Enter Quantity: 5
✅ Book added successfully!
```

#### Registering a User
```
1. Select Option: 2 (Add User)
2. Enter User ID: U001
3. Enter Full Name: John Doe
4. Enter Email: john.doe@example.com
5. Enter Phone: 9876543210
✅ User created successfully!
```

#### Issuing a Book
```
1. Select Option: 3 (Issue Book)
2. Enter User ID: U001
3. Enter Book ID: B001
4. Enter Issue Duration: 14
✅ Book issued successfully!
   Due Date: 18-06-2026
```

#### Returning a Book
```
1. Select Option: 4 (Return Book)
2. Enter User ID: U001
3. Enter Book ID: B001
✅ Book returned successfully!
   Fine Amount: ₹0.00 (No fine - returned on time)
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Books Table
```sql
CREATE TABLE books (
    book_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    isbn TEXT UNIQUE,
    total_quantity INTEGER NOT NULL,
    available_quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Transactions Table
```sql
CREATE TABLE transactions (
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
```

## 🎓 OOP Concepts Demonstrated

### 1. **Abstraction**
- Abstract base class `Entity` defining common interface
- Abstract methods: `to_dict()`, `validate()`, `get_id()`
- Concrete implementations in `User`, `Book`, `Transaction` classes

### 2. **Encapsulation**
- Private attributes (prefixed with `_`)
- Read-only properties using `@property` decorators
- Data validation in constructors

### 3. **Inheritance**
- `User`, `Book`, `Transaction` inherit from `Entity`
- Common interface enforced through inheritance

### 4. **Polymorphism**
- Multiple implementations of abstract methods
- Different behavior for `to_dict()` and `validate()` in each class
- Type-appropriate implementations across entity classes

### Example Code
```python
# Abstract Base Class - Abstraction
class Entity(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

# Concrete Implementation - Inheritance & Encapsulation
class User(Entity):
    def __init__(self, user_id: str, name: str):
        self._user_id = user_id      # Private attribute
        self._name = name
    
    @property
    def user_id(self) -> str:        # Encapsulation via property
        return self._user_id
    
    def to_dict(self) -> Dict:       # Polymorphism
        return {"id": self._user_id, "name": self._name}
```

## 💰 Fine Calculation Policy

### Policy Details

| Condition | Fine |
|-----------|------|
| Returned on or before due date | ₹0.00 |
| 1-7 days overdue | ₹0.00 (Grace Period) |
| 8+ days overdue | ₹5.00 per day |

### Example Calculations

- **Scenario 1**: Due date: 18-06-2026, Returned: 18-06-2026
  - Status: On time
  - Fine: ₹0.00

- **Scenario 2**: Due date: 18-06-2026, Returned: 25-06-2026 (7 days late)
  - Days overdue: 7 days
  - Status: Within grace period
  - Fine: ₹0.00

- **Scenario 3**: Due date: 18-06-2026, Returned: 28-06-2026 (10 days late)
  - Days overdue: 10 days
  - Grace period: 7 days
  - Chargeable days: 3 days
  - Fine: 3 × ₹5 = **₹15.00**

## 🛡️ Exception Handling

Custom exception hierarchy for precise error handling:

```
LibraryException (Base)
├── UserException
│   ├── UserNotFoundError
│   ├── UserAlreadyExistsError
│   └── InvalidUserDataError
├── BookException
│   ├── BookNotFoundError
│   ├── BookAlreadyExistsError
│   ├── InsufficientBookQuantityError
│   └── InvalidBookDataError
├── TransactionException
│   ├── InvalidTransactionError
│   └── BookNotIssuedError
├── FineException
│   └── InvalidFineDataError
└── DatabaseException
```

## 📊 Code Quality Features

### PEP8 Compliance
- ✅ Proper naming conventions (snake_case, PascalCase)
- ✅ Line length < 100 characters
- ✅ Proper spacing and indentation
- ✅ Type hints throughout

### Documentation
- ✅ Module-level docstrings
- ✅ Class docstrings with descriptions
- ✅ Method docstrings with Args, Returns, Raises sections
- ✅ Inline comments for complex logic

### Validation
- ✅ Input validation in all constructors
- ✅ Exception handling for all operations
- ✅ Boundary condition checks
- ✅ Database constraint enforcement

## 🧪 Testing Recommendations

### Test Scenarios

```python
# Test User Creation
user = library.add_user("U001", "John Doe", "john@example.com")
assert user.user_id == "U001"

# Test Book Addition
book = library.add_book("B001", "Python", "Guido", "123456", 5)
assert book.available_quantity == 5

# Test Issue and Return
transaction = library.issue_book("U001", "B001")
assert transaction.status == "active"

returned = library.return_book("U001", "B001")
assert returned.fine_amount >= 0
```

## 🤝 Contributing Guidelines

When extending this project:

1. **Maintain OOP Principles**: Add new features as classes or methods
2. **Follow PEP8**: Use consistent formatting and naming
3. **Add Docstrings**: Document all new public methods
4. **Handle Exceptions**: Use custom exceptions for error cases
5. **Update Tests**: Add test cases for new functionality

## 📋 Feature Enhancements (Future Scope)

- [ ] Web interface (Flask/Django)
- [ ] Email notifications for overdue books
- [ ] Book reservations system
- [ ] Multi-branch support
- [ ] Advanced analytics and reports
- [ ] User authentication system
- [ ] REST API
- [ ] Export to PDF/Excel

## 📝 License

This is an educational project. Feel free to use and modify for learning purposes.

## 👨‍💻 Author

Created as a portfolio project demonstrating Python OOP and Database Management.

## 📚 Learning Resources

### OOP Concepts
- [Real Python - OOP](https://realpython.com/python3-object-oriented-programming/)
- [Python ABC Module](https://docs.python.org/3/library/abc.html)

### Database
- [SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Database Design Basics](https://www.studytonight.com/sql/database-design)

### Code Quality
- [PEP8 Style Guide](https://pep8.org/)
- [Python Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)

## ❓ FAQ

**Q: How do I backup my library data?**
A: The `library_system.db` file contains all data. Back up this file to preserve your library database.

**Q: Can I change the fine policy?**
A: Yes! Modify the constants in `fine_manager.py`:
```python
GRACE_PERIOD_DAYS = 7  # Change grace period
FINE_PER_DAY = 5       # Change fine amount
```

**Q: How many users and books can the system handle?**
A: SQLite can handle millions of records efficiently. The system is designed for production use.

**Q: Is the data persistent?**
A: Yes! All data is stored in SQLite database and persists between sessions.

**Q: Can I export transaction history?**
A: Currently, you can view history on screen. Export functionality can be added by extending the `OperationsManager` class.

---

**Happy Learning! 📚** 

For questions or improvements, feel free to extend and modify the code according to your requirements.
- Searching for books by name.
- Adding new users to the system.
- Borrowing books.
- Returning books.
- Printing users who borrowed books.
- Printing all users in the system.

## Features

- **Add Books**: Easily add new books to the library with unique IDs.
- **Manage Users**: Add new users to the system for tracking borrowing activities.
- **Search Books**: Search for books by name using a prefix.
- **Borrow and Return**: Borrow books from the library and return them when done.
- **Track Borrowers**: Keep track of users who have borrowed books.
- **User Interface**: Simple command-line interface for user interaction.


