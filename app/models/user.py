import bcrypt
import mysql.connector
from mysql.connector import Error
import sys
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

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_setup import get_connection

class User:
    def __init__(self, id=None, name=None, email=None, password_hash=None, role_id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id

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
    def create_user(email, password, first_name, last_name, phone=None, address=None, role_id=2):
        """Create a new user in the database."""
        connection = User.get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already registered"
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert the new user
            cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, phone, address, role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (email, hashed_password.decode('utf-8'), first_name, last_name, phone, address, role_id))
            
            connection.commit()
            user_id = cursor.lastrowid
            
            # Create a User object for the new user
            user = User(
                id=user_id,
                name=f"{first_name} {last_name}",
                email=email,
                password_hash=hashed_password.decode('utf-8'),
                role_id=role_id
            )
            
            return True, user
        except Error as e:
            print(f"Error creating user: {e}")
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def authenticate(email, password):
        """Authenticate a user."""
        connection = User.get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get user by email
            cursor.execute("""
            SELECT id, email, password_hash, first_name, last_name, role_id
            FROM users WHERE email = %s
            """, (email,))
            
            user_data = cursor.fetchone()
            
            if not user_data:
                return False, "Invalid email or password"
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
                # Create user object
                user = User(
                    id=user_data['id'],
                    name=f"{user_data['first_name']} {user_data['last_name']}",
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    role_id=user_data['role_id']
                )
                return True, user
            else:
                return False, "Invalid email or password"
        except Error as e:
            print(f"Error authenticating user: {e}")
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID."""
        connection = User.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("""
            SELECT id, email, first_name, last_name, role_id
            FROM users WHERE id = %s
            """, (user_id,))
            
            user_data = cursor.fetchone()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=f"{user_data['first_name']} {user_data['last_name']}",
                    email=user_data['email'],
                    role_id=user_data['role_id']
                )
            return None
        except Error as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_clients_for_admin(admin_id):
        """Get all clients assigned to an admin."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT u.id, u.email, u.first_name, u.last_name, u.phone, u.address, u.role_id
            FROM users u
            JOIN user_assignments ua ON u.id = ua.client_id
            WHERE ua.admin_id = %s
            """
            cursor.execute(query, (admin_id,))
            clients_data = cursor.fetchall()
            
            clients = []
            for client_data in clients_data:
                client = User(
                    id=client_data['id'],
                    email=client_data['email'],
                    first_name=client_data['first_name'],
                    last_name=client_data['last_name'],
                    phone=client_data['phone'],
                    address=client_data['address'],
                    role_id=client_data['role_id']
                )
                clients.append(client)
            
            return clients
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def assign_client_to_admin(admin_id, client_id):
        """Assign a client to an admin."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if admin is actually an admin
            cursor.execute("SELECT role_id FROM users WHERE id = %s", (admin_id,))
            admin = cursor.fetchone()
            if not admin or admin[0] != 1:  # 1 is admin role_id
                return False, "User is not an admin"
            
            # Check if client is actually a client
            cursor.execute("SELECT role_id FROM users WHERE id = %s", (client_id,))
            client = cursor.fetchone()
            if not client or client[0] != 2:  # 2 is client role_id
                return False, "User is not a client"
            
            # Create the assignment
            query = """
            INSERT INTO user_assignments (admin_id, client_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE assigned_at = CURRENT_TIMESTAMP
            """
            cursor.execute(query, (admin_id, client_id))
            connection.commit()
            
            return True, "Client assigned to admin"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_profile(self, first_name=None, last_name=None, phone=None, address=None):
        """Update user profile information."""
        if not self.id:
            return False, "User ID not set"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Update only the fields that are provided
            updates = []
            params = []
            
            if first_name is not None:
                updates.append("first_name = %s")
                params.append(first_name)
                self.first_name = first_name
                
            if last_name is not None:
                updates.append("last_name = %s")
                params.append(last_name)
                self.last_name = last_name
                
            if phone is not None:
                updates.append("phone = %s")
                params.append(phone)
                self.phone = phone
                
            if address is not None:
                updates.append("address = %s")
                params.append(address)
                self.address = address
                
            if not updates:
                return True, "No updates provided"
                
            # Add the user ID to the parameters
            params.append(self.id)
            
            # Create and execute the update query
            query = f"""
            UPDATE users
            SET {', '.join(updates)}
            WHERE id = %s
            """
            cursor.execute(query, params)
            connection.commit()
            
            return True, "Profile updated successfully"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def change_password(self, current_password, new_password):
        """Change user password."""
        if not self.id:
            return False, "User ID not set"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get the current password hash
            cursor.execute("SELECT password_hash FROM users WHERE id = %s", (self.id,))
            result = cursor.fetchone()
            
            if not result:
                return False, "User not found"
                
            # Verify the current password
            if not bcrypt.checkpw(current_password.encode('utf-8'), result['password_hash'].encode('utf-8')):
                return False, "Current password is incorrect"
                
            # Hash and update the new password
            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash.decode('utf-8'), self.id))
            connection.commit()
            
            return True, "Password changed successfully"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def is_admin(self):
        """Check if user is an admin."""
        return self.role_id == 1 