# 📚 Project File Reference Guide

## Quick Reference - What Each File Does

### Core Application Files

#### 🗄️ `database.py`
**Purpose**: Database connection management and schema initialization
**Key Classes**: `DatabaseManager`, `DatabaseError`
**Responsibilities**:
- SQLite connection handling with context managers
- Automatic schema creation on first run
- Query execution methods (SELECT, INSERT, UPDATE, DELETE)
- Connection pooling

**Key Methods**:
- `_initialize_database()` - Create tables if needed
- `get_db_context()` - Context manager for safe DB operations
- `execute_query()` - Run SELECT queries
- `execute_update()` - Run INSERT/UPDATE/DELETE queries
- `execute_insert()` - Insert and get ID

---

#### 🎯 `models.py`
**Purpose**: OOP entity definitions with proper encapsulation
**Key Classes**: `Entity`, `User`, `Book`, `Transaction`
**Demonstrates**:
- Abstraction (ABC with abstract methods)
- Encapsulation (private attributes with @property)
- Inheritance (User/Book/Transaction inherit from Entity)
- Polymorphism (different to_dict() implementations)

**Key Methods**:
- `Entity.validate()` - Abstract validation method
- `User.__init__()` - User creation with validation
- `Book.decrease_available_quantity()` - Manage quantities
- `Transaction.is_overdue()` - Check overdue status

---

#### ⚡ `exceptions.py`
**Purpose**: Custom exception hierarchy for error handling
**Exception Hierarchy**:
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

---

#### 💰 `fine_manager.py`
**Purpose**: Automated fine calculation logic
**Key Classes**: `FineManager`
**Fine Policy**:
- Days 1-7 after due date: Free (grace period)
- Day 8+: ₹5 per day

**Key Methods**:
- `calculate_fine()` - Calculate fine for given dates
- `is_overdue()` - Check if overdue
- `get_days_overdue()` - Days past due date
- `get_days_until_due()` - Days remaining
- `format_fine_display()` - Format for display (₹X.XX)

---

#### 📖 `library.py`
**Purpose**: Core business logic and main library management
**Key Classes**: `Library`
**Manages**:
- User operations (add, search, get)
- Book operations (add, search, remove)
- Transactions (issue, return books)
- Fine calculations
- Statistics and reporting

**Key Methods**:
```python
# User Operations
add_user(user_id, name, email, phone) -> User
get_user(user_id) -> User
search_users(name) -> List[User]
get_all_users() -> List[User]

# Book Operations
add_book(book_id, title, author, isbn, qty) -> Book
get_book(book_id) -> Book
search_books(query) -> List[Book]
get_available_books() -> List[Book]
remove_book(book_id) -> None

# Transaction Operations
issue_book(user_id, book_id, days) -> Transaction
return_book(user_id, book_id) -> Transaction
get_user_issued_books(user_id) -> List[Dict]
get_transaction_history(user_id, book_id, status) -> List[Dict]
get_overdue_books() -> List[Dict]

# Reporting
get_library_statistics() -> Dict
```

---

#### 🎮 `operations_manager.py`
**Purpose**: CLI user interface and menu management
**Key Classes**: `OperationsManager`
**Features**:
- Interactive menu system
- Input validation
- Formatted output
- Admin panel
- Error handling with user-friendly messages

**Main Methods**:
- `display_menu()` - Show main menu
- `add_book()` - Handle book addition
- `add_user()` - Handle user registration
- `issue_book()` - Handle book lending
- `return_book()` - Handle book return
- `search_books()` - Search functionality
- `view_statistics()` - Display stats
- `run()` - Main application loop

---

#### 🚀 `main.py`
**Purpose**: Application entry point
**Responsibilities**:
- Initialize OperationsManager
- Handle KeyboardInterrupt
- Graceful error handling
- Application startup

**Usage**:
```bash
python main.py
```

---

#### 🧪 `demo.py`
**Purpose**: Feature demonstration and verification script
**Demonstrates**:
- User management
- Book management
- Transaction handling
- Fine calculations
- Exception handling
- All features in action

**Run with**:
```bash
python demo.py
```

---

### Documentation Files

#### 📖 `readme.md`
**Purpose**: Professional project documentation
**Contains**:
- Project overview and features
- Installation and setup instructions
- Usage guide with examples
- Database schema documentation
- OOP concepts explanation
- Fine calculation policy
- FAQ section
- Learning resources

---

#### 📊 `UPGRADE_SUMMARY.md`
**Purpose**: Complete upgrade summary and talking points
**Contains**:
- What was accomplished
- Before/after comparisons
- OOP improvements explained
- Code quality metrics
- Interview preparation notes
- Resume impact summary
- Quick command reference

---

## 🎯 Quick Start Guide

### 1. First Run
```bash
python main.py
```

### 2. Demo/Testing
```bash
python demo.py
```

### 3. View Code Quality
```bash
# Check for syntax errors
python -m py_compile *.py

# List all Python files
ls *.py
```

---

## 📋 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| database.py | 85 | DB Management |
| models.py | 450+ | OOP Entities |
| exceptions.py | 80+ | Error Handling |
| fine_manager.py | 130+ | Fine Calculation |
| library.py | 500+ | Business Logic |
| operations_manager.py | 600+ | UI/CLI |
| main.py | 30 | Entry Point |
| demo.py | 280+ | Testing/Demo |
| readme.md | 400+ | Documentation |
| UPGRADE_SUMMARY.md | 350+ | Summary |

**Total**: 2,900+ lines of professional code

---

## 🔗 File Dependencies

```
main.py
  └── operations_manager.py
      └── library.py
          ├── models.py
          │   └── exceptions.py
          ├── fine_manager.py
          ├── database.py
          │   └── exceptions.py
          └── exceptions.py
```

---

## 🎓 Learning Path

### Understand the System
1. Read `readme.md` for overview
2. Read `UPGRADE_SUMMARY.md` for details
3. Run `demo.py` to see features in action

### Study the Code
1. Start with `models.py` to understand OOP
2. Review `exceptions.py` for error handling
3. Study `library.py` for business logic
4. Examine `database.py` for DB operations

### Extend the System
1. Add new features in `library.py`
2. Update `operations_manager.py` for new menus
3. Add exceptions to `exceptions.py` as needed
4. Keep `models.py` clean and focused

---

## 🚀 Common Operations

### Run the Application
```bash
python main.py
```

### Run Tests/Demo
```bash
python demo.py
```

### Check Syntax
```bash
python -m py_compile *.py
```

### View Database
```bash
# Install sqlite3 browser or use Python
python -c "import sqlite3; conn = sqlite3.connect('library_system.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM users'); print(cursor.fetchall())"
```

### Reset Database
```bash
# Delete database file to start fresh
rm library_system.db
python main.py
```

---

## 💡 Pro Tips

### For Interviews
1. **Know the OOP hierarchy**: Entity → User/Book/Transaction
2. **Explain the fine logic**: 7-day grace period + ₹5/day
3. **Discuss database schema**: 3 tables with foreign keys
4. **Show code quality**: PEP8, type hints, docstrings

### For Extensions
1. **Add logging**: Import logging module in each file
2. **Add authentication**: Extend User model
3. **Add web UI**: Use Flask/Django with current models
4. **Add testing**: Create test_*.py files

### For Optimization
1. **Add indexes**: `database.py` has them, verify with EXPLAIN QUERY PLAN
2. **Add caching**: Cache frequent queries
3. **Add pagination**: For large result sets
4. **Add bulk operations**: For multiple inserts

---

## 🎉 What You Have

A complete, production-ready library management system that demonstrates:

✅ Advanced Python OOP (4 principles)
✅ Professional Database Design
✅ Comprehensive Exception Handling
✅ Clean Code Practices
✅ Complete Documentation
✅ Real-world Features
✅ Interview-ready Code

This is a **strong portfolio project**! 🚀

---

## 📞 Quick Reference Commands

```bash
# Start the application
python main.py

# Run demonstration
python demo.py

# Check syntax
python -m py_compile *.py

# List Python files
dir *.py  # Windows
ls *.py   # Linux/Mac

# View file sizes
wc -l *.py  # Linux/Mac
```

---

**Ready to impress! 💪**
