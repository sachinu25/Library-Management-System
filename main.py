"""
Main entry point for the Library Management System.

This module initializes and runs the library management application.
Demonstrates proper application initialization and error handling.
"""

import sys
from operations_manager import OperationsManager


def main() -> None:
    """
    Main entry point for the application.
    
    Initializes and runs the OperationsManager to start the CLI.
    """
    try:
        manager = OperationsManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

