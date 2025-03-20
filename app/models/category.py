import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_setup import get_connection

class Category:
    def __init__(self, id=None, category_name=None, is_expense=True, icon=None, color=None, parent_category_id=None):
        self.id = id
        self.category_name = category_name
        self.is_expense = is_expense
        self.icon = icon
        self.color = color
        self.parent_category_id = parent_category_id
        self._parent_category_name = None  # For caching

    @staticmethod
    def get_all_categories(is_expense=None):
        """Get all categories, optionally filtered by expense/income type."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, category_name, is_expense, icon, color, parent_category_id
            FROM transaction_categories
            """
            params = []
            
            if is_expense is not None:
                query += " WHERE is_expense = %s"
                params.append(is_expense)
                
            query += " ORDER BY category_name"
            
            cursor.execute(query, params)
            categories_data = cursor.fetchall()
            
            categories = []
            for cat_data in categories_data:
                category = Category(
                    id=cat_data['id'],
                    category_name=cat_data['category_name'],
                    is_expense=cat_data['is_expense'],
                    icon=cat_data['icon'],
                    color=cat_data['color'],
                    parent_category_id=cat_data['parent_category_id']
                )
                categories.append(category)
            
            return categories
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(category_id):
        """Get a category by ID."""
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, category_name, is_expense, icon, color, parent_category_id
            FROM transaction_categories
            WHERE id = %s
            """
            cursor.execute(query, (category_id,))
            cat_data = cursor.fetchone()
            
            if not cat_data:
                return None
            
            return Category(
                id=cat_data['id'],
                category_name=cat_data['category_name'],
                is_expense=cat_data['is_expense'],
                icon=cat_data['icon'],
                color=cat_data['color'],
                parent_category_id=cat_data['parent_category_id']
            )
            
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def create_category(category_name, is_expense, icon=None, color=None, parent_category_id=None):
        """Create a new category."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if category name already exists
            cursor.execute("SELECT id FROM transaction_categories WHERE category_name = %s", (category_name,))
            if cursor.fetchone():
                return False, "Category name already exists"
            
            # Insert the category
            query = """
            INSERT INTO transaction_categories (category_name, is_expense, icon, color, parent_category_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (category_name, is_expense, icon, color, parent_category_id))
            connection.commit()
            
            # Get the category id
            category_id = cursor.lastrowid
            
            return True, category_id
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self, category_name=None, is_expense=None, icon=None, color=None, parent_category_id=None):
        """Update category information."""
        if not self.id:
            return False, "Category ID not set"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Update only the fields that are provided
            updates = []
            params = []
            
            if category_name is not None:
                # Check if name already exists for other categories
                cursor.execute(
                    "SELECT id FROM transaction_categories WHERE category_name = %s AND id != %s", 
                    (category_name, self.id)
                )
                if cursor.fetchone():
                    return False, "Category name already exists"
                    
                updates.append("category_name = %s")
                params.append(category_name)
                self.category_name = category_name
                
            if is_expense is not None:
                updates.append("is_expense = %s")
                params.append(is_expense)
                self.is_expense = is_expense
                
            if icon is not None:
                updates.append("icon = %s")
                params.append(icon)
                self.icon = icon
                
            if color is not None:
                updates.append("color = %s")
                params.append(color)
                self.color = color
                
            if parent_category_id is not None:
                # Don't allow circular references
                if parent_category_id == self.id:
                    return False, "Category cannot be its own parent"
                    
                updates.append("parent_category_id = %s")
                params.append(parent_category_id)
                self.parent_category_id = parent_category_id
                self._parent_category_name = None  # Reset cached value
                
            if not updates:
                return True, "No updates provided"
                
            # Add the category ID to the parameters
            params.append(self.id)
            
            # Create and execute the update query
            query = f"""
            UPDATE transaction_categories
            SET {', '.join(updates)}
            WHERE id = %s
            """
            cursor.execute(query, params)
            connection.commit()
            
            return True, "Category updated successfully"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_category(category_id):
        """Delete a category."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if the category is in use in any transactions
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE category_id = %s", (category_id,))
            if cursor.fetchone()[0] > 0:
                return False, "Category is in use and cannot be deleted"
                
            # Check if the category has any child categories
            cursor.execute("SELECT COUNT(*) FROM transaction_categories WHERE parent_category_id = %s", (category_id,))
            if cursor.fetchone()[0] > 0:
                return False, "Category has child categories and cannot be deleted"
            
            # Delete the category
            cursor.execute("DELETE FROM transaction_categories WHERE id = %s", (category_id,))
            connection.commit()
            
            return True, "Category deleted successfully"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @property
    def parent_category_name(self):
        """Get the parent category name."""
        if self._parent_category_name is None and self.parent_category_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT category_name FROM transaction_categories WHERE id = %s", (self.parent_category_id,))
                    result = cursor.fetchone()
                    if result:
                        self._parent_category_name = result['category_name']
                except Error as e:
                    print(f"Error getting parent category name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._parent_category_name

    @staticmethod
    def get_subcategories(parent_category_id):
        """Get all subcategories for a given parent category."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, category_name, is_expense, icon, color, parent_category_id
            FROM transaction_categories
            WHERE parent_category_id = %s
            ORDER BY category_name
            """
            cursor.execute(query, (parent_category_id,))
            categories_data = cursor.fetchall()
            
            categories = []
            for cat_data in categories_data:
                category = Category(
                    id=cat_data['id'],
                    category_name=cat_data['category_name'],
                    is_expense=cat_data['is_expense'],
                    icon=cat_data['icon'],
                    color=cat_data['color'],
                    parent_category_id=cat_data['parent_category_id']
                )
                categories.append(category)
            
            return categories
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_top_level_categories(is_expense=None):
        """Get all top-level categories (with no parent)."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, category_name, is_expense, icon, color, parent_category_id
            FROM transaction_categories
            WHERE parent_category_id IS NULL
            """
            params = []
            
            if is_expense is not None:
                query += " AND is_expense = %s"
                params.append(is_expense)
                
            query += " ORDER BY category_name"
            
            cursor.execute(query, params)
            categories_data = cursor.fetchall()
            
            categories = []
            for cat_data in categories_data:
                category = Category(
                    id=cat_data['id'],
                    category_name=cat_data['category_name'],
                    is_expense=cat_data['is_expense'],
                    icon=cat_data['icon'],
                    color=cat_data['color'],
                    parent_category_id=cat_data['parent_category_id']
                )
                categories.append(category)
            
            return categories
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 