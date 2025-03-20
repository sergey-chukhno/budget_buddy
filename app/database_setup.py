import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '3306')
}

DB_NAME = os.getenv('DB_NAME', 'billionnaires_budget_buddy')

def create_database():
    """Create the database if it doesn't exist."""
    connection = None
    cursor = None
    try:
        print("Attempting to connect to MySQL with the following config:")
        print(f"Host: {DB_CONFIG['host']}, User: {DB_CONFIG['user']}, Port: {DB_CONFIG['port']}")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")
        
        # Switch to the database
        cursor.execute(f"USE {DB_NAME}")
        
        # Create tables
        create_tables(cursor)
        
        # Create default admin account
        create_default_admin(cursor)
        
        # Create default categories
        create_default_categories(cursor)
        
        # Create default account types
        create_default_account_types(cursor)
        
        connection.commit()
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def create_tables(cursor):
    """Create all required tables for the application."""
    
    # User Roles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_roles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT
    )
    """)
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20),
        address TEXT,
        role_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES user_roles(id)
    )
    """)
    
    # User Assignments (admin to clients)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        admin_id INT NOT NULL,
        client_id INT NOT NULL,
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (admin_id) REFERENCES users(id),
        FOREIGN KEY (client_id) REFERENCES users(id),
        UNIQUE KEY unique_assignment (admin_id, client_id)
    )
    """)
    
    # Account Types
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT
    )
    """)
    
    # Accounts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        account_type_id INT NOT NULL,
        account_name VARCHAR(100) NOT NULL,
        balance DECIMAL(15, 2) DEFAULT 0.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (account_type_id) REFERENCES account_types(id)
    )
    """)
    
    # Transaction Categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL,
        is_expense BOOLEAN NOT NULL,
        icon VARCHAR(100),
        color VARCHAR(20),
        parent_category_id INT,
        FOREIGN KEY (parent_category_id) REFERENCES transaction_categories(id)
    )
    """)
    
    # Transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_id INT NOT NULL,
        category_id INT,
        amount DECIMAL(15, 2) NOT NULL,
        transaction_type ENUM('deposit', 'withdrawal', 'transfer', 'external_transfer') NOT NULL,
        description TEXT,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by_user_id INT NOT NULL,
        recipient_account_id INT,
        external_recipient VARCHAR(255),
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (category_id) REFERENCES transaction_categories(id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(id),
        FOREIGN KEY (recipient_account_id) REFERENCES accounts(id)
    )
    """)
    
    # Transaction Audit Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_audit_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaction_id INT NOT NULL,
        user_id INT NOT NULL,
        action VARCHAR(50) NOT NULL,
        action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details TEXT,
        FOREIGN KEY (transaction_id) REFERENCES transactions(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    # Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        setting_key VARCHAR(100) NOT NULL,
        setting_value TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        UNIQUE KEY unique_user_setting (user_id, setting_key)
    )
    """)
    
    print("All tables created successfully")

def create_default_admin(cursor):
    """Create a default admin account if none exists."""
    # First check if roles exist
    cursor.execute("SELECT COUNT(*) FROM user_roles")
    if cursor.fetchone()[0] == 0:
        # Insert roles
        roles = [
            (1, 'admin', 'Administrative user with full system access'),
            (2, 'client', 'Regular client user')
        ]
        cursor.executemany("INSERT INTO user_roles (id, role_name, description) VALUES (%s, %s, %s)", roles)
    
    # Check if admin exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE role_id = 1")
    if cursor.fetchone()[0] == 0:
        # Create default admin
        default_password = "admin123"  # In production, use a secure password
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        
        admin = (
            'admin@billionnaires.com',
            hashed_password.decode('utf-8'),
            'Admin',
            'User',
            '123-456-7890',
            'Admin Address',
            1  # admin role_id
        )
        
        cursor.execute("""
        INSERT INTO users (email, password_hash, first_name, last_name, phone, address, role_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, admin)
        
        print("Default admin user created")

def create_default_categories(cursor):
    """Create default transaction categories."""
    cursor.execute("SELECT COUNT(*) FROM transaction_categories")
    if cursor.fetchone()[0] == 0:
        # Income categories
        income_categories = [
            ('Salary', False, 'salary', '#4CAF50', None),
            ('Investment', False, 'investment', '#8BC34A', None),
            ('Gift', False, 'gift', '#CDDC39', None),
            ('Other Income', False, 'other_income', '#FFC107', None)
        ]
        
        # Expense categories
        expense_categories = [
            ('Food & Dining', True, 'food', '#F44336', None),
            ('Shopping', True, 'shopping', '#E91E63', None),
            ('Housing', True, 'home', '#9C27B0', None),
            ('Transportation', True, 'car', '#673AB7', None),
            ('Entertainment', True, 'entertainment', '#3F51B5', None),
            ('Health & Fitness', True, 'health', '#2196F3', None),
            ('Education', True, 'education', '#03A9F4', None),
            ('Utilities', True, 'utilities', '#00BCD4', None),
            ('Travel', True, 'travel', '#009688', None),
            ('Other Expenses', True, 'other_expense', '#FF5722', None)
        ]
        
        # Insert income categories
        for category in income_categories:
            cursor.execute("""
            INSERT INTO transaction_categories (category_name, is_expense, icon, color, parent_category_id)
            VALUES (%s, %s, %s, %s, %s)
            """, category)
            
        # Insert expense categories
        for category in expense_categories:
            cursor.execute("""
            INSERT INTO transaction_categories (category_name, is_expense, icon, color, parent_category_id)
            VALUES (%s, %s, %s, %s, %s)
            """, category)
            
        print("Default categories created")

def create_default_account_types(cursor):
    """Create default account types."""
    cursor.execute("SELECT COUNT(*) FROM account_types")
    if cursor.fetchone()[0] == 0:
        account_types = [
            ('Checking', 'Everyday spending account'),
            ('Savings', 'Account for saving money with interest'),
            ('Investment', 'Account for investing in stocks, bonds, etc.'),
            ('Credit Card', 'Credit card account with monthly payments')
        ]
        
        for account_type in account_types:
            cursor.execute("""
            INSERT INTO account_types (type_name, description)
            VALUES (%s, %s)
            """, account_type)
            
        print("Default account types created")

def get_connection():
    """Get a connection to the database."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DB_NAME
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    create_database() 