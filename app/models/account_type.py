import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '3306'),
    'database': os.getenv('DB_NAME', 'billionnaires_budget_buddy')
}

class AccountType:
    def __init__(self, id=None, type_name=None, description=None):
        self.id = id
        self.type_name = type_name
        self.description = description

    @staticmethod
    def get_connection():
        """Get a database connection."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    @staticmethod
    def get_all_account_types():
        """Get all account types from the database."""
        connection = AccountType.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("""
            SELECT id, type_name, description 
            FROM account_types
            ORDER BY type_name
            """)
            
            account_types_data = cursor.fetchall()
            
            # Convert to AccountType objects
            account_types = []
            for data in account_types_data:
                account_type = AccountType(
                    id=data['id'],
                    type_name=data['type_name'],
                    description=data['description']
                )
                account_types.append(account_type)
                
            return account_types
        except Error as e:
            print(f"Error getting account types: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_account_type_by_id(account_type_id):
        """Get an account type by ID."""
        connection = AccountType.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("""
            SELECT id, type_name, description 
            FROM account_types 
            WHERE id = %s
            """, (account_type_id,))
            
            account_type = cursor.fetchone()
            if account_type:
                return AccountType(
                    id=account_type['id'],
                    type_name=account_type['type_name'],
                    description=account_type['description']
                )
            return None
        except Error as e:
            print(f"Error getting account type: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def create_account_type(type_name, description=None):
        """Create a new account type."""
        connection = AccountType.get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if account type already exists
            cursor.execute("SELECT id FROM account_types WHERE type_name = %s", (type_name,))
            if cursor.fetchone():
                return False, "Account type already exists"
            
            # Insert the new account type
            cursor.execute("""
            INSERT INTO account_types (type_name, description)
            VALUES (%s, %s)
            """, (type_name, description))
            
            connection.commit()
            account_type_id = cursor.lastrowid
            
            return True, account_type_id
        except Error as e:
            print(f"Error creating account type: {e}")
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 