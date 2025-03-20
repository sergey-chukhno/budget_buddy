import bcrypt
import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_setup import get_connection

class User:
    def __init__(self, id=None, email=None, first_name=None, last_name=None, phone=None, address=None, role_id=None):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.role_id = role_id

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against a provided password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    @staticmethod
    def register(email, password, first_name, last_name, phone, address, role_id=2):  # Default role is client
        """Register a new user."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already exists"
            
            # Hash the password
            hashed_password = User.hash_password(password)
            
            # Insert the user
            query = """
            INSERT INTO users (email, password_hash, first_name, last_name, phone, address, role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (email, hashed_password, first_name, last_name, phone, address, role_id))
            connection.commit()
            
            # Get the user id
            user_id = cursor.lastrowid
            
            return True, user_id
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def login(email, password):
        """Login a user."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get the user
            query = """
            SELECT id, email, password_hash, first_name, last_name, phone, address, role_id
            FROM users
            WHERE email = %s
            """
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            if not user:
                return False, "Invalid email or password"
            
            # Verify the password
            if not User.verify_password(user['password_hash'], password):
                return False, "Invalid email or password"
            
            # Create a user object
            user_obj = User(
                id=user['id'],
                email=user['email'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                phone=user['phone'],
                address=user['address'],
                role_id=user['role_id']
            )
            
            return True, user_obj
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(user_id):
        """Get a user by ID."""
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, email, first_name, last_name, phone, address, role_id
            FROM users
            WHERE id = %s
            """
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return None
            
            return User(
                id=user_data['id'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                role_id=user_data['role_id']
            )
            
        except Error as e:
            print(f"Error: {e}")
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
            if not User.verify_password(result['password_hash'], current_password):
                return False, "Current password is incorrect"
                
            # Hash and update the new password
            new_hash = User.hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, self.id))
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