import mysql.connector
from mysql.connector import Error
import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_setup import get_connection

class Transaction:
    def __init__(self, id=None, account_id=None, category_id=None, amount=0.0, transaction_type=None, 
                 description=None, transaction_date=None, created_by_user_id=None, 
                 recipient_account_id=None, external_recipient=None):
        self.id = id
        self.account_id = account_id
        self.category_id = category_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.transaction_date = transaction_date
        self.created_by_user_id = created_by_user_id
        self.recipient_account_id = recipient_account_id
        self.external_recipient = external_recipient
        
        # For caching related data
        self._account_name = None
        self._category_name = None
        self._recipient_account_name = None
        self._created_by_name = None

    @staticmethod
    def get_by_id(transaction_id):
        """Get a transaction by ID."""
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, account_id, category_id, amount, transaction_type, description, 
                   transaction_date, created_by_user_id, recipient_account_id, external_recipient
            FROM transactions
            WHERE id = %s
            """
            cursor.execute(query, (transaction_id,))
            txn_data = cursor.fetchone()
            
            if not txn_data:
                return None
            
            return Transaction(
                id=txn_data['id'],
                account_id=txn_data['account_id'],
                category_id=txn_data['category_id'],
                amount=float(txn_data['amount']),
                transaction_type=txn_data['transaction_type'],
                description=txn_data['description'],
                transaction_date=txn_data['transaction_date'],
                created_by_user_id=txn_data['created_by_user_id'],
                recipient_account_id=txn_data['recipient_account_id'],
                external_recipient=txn_data['external_recipient']
            )
            
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_transactions_for_account(account_id, limit=100, offset=0, start_date=None, end_date=None, 
                                     category_id=None, search_term=None, transaction_type=None,
                                     min_amount=None, max_amount=None, include_details=False):
        """Get transactions for an account with filtering options."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Base query
            if include_details:
                query = """
                SELECT t.id, t.account_id, t.category_id, t.amount, t.transaction_type, t.description, 
                       t.transaction_date, t.created_by_user_id, t.recipient_account_id, t.external_recipient,
                       a.account_name, 
                       tc.category_name, tc.is_expense, tc.icon, tc.color,
                       ra.account_name as recipient_account_name,
                       CONCAT(u.first_name, ' ', u.last_name) as created_by_name
                FROM transactions t
                LEFT JOIN accounts a ON t.account_id = a.id
                LEFT JOIN transaction_categories tc ON t.category_id = tc.id
                LEFT JOIN accounts ra ON t.recipient_account_id = ra.id
                LEFT JOIN users u ON t.created_by_user_id = u.id
                """
            else:
                query = """
                SELECT id, account_id, category_id, amount, transaction_type, description, 
                       transaction_date, created_by_user_id, recipient_account_id, external_recipient
                FROM transactions
                """
            
            # Build where clause and parameters
            where_clauses = ["(account_id = %s OR recipient_account_id = %s)"]
            params = [account_id, account_id]
            
            if start_date:
                where_clauses.append("transaction_date >= %s")
                params.append(start_date)
                
            if end_date:
                where_clauses.append("transaction_date <= %s")
                params.append(end_date)
                
            if category_id:
                where_clauses.append("category_id = %s")
                params.append(category_id)
                
            if search_term:
                where_clauses.append("(description LIKE %s OR external_recipient LIKE %s)")
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
                
            if transaction_type:
                where_clauses.append("transaction_type = %s")
                params.append(transaction_type)
                
            if min_amount is not None:
                where_clauses.append("amount >= %s")
                params.append(min_amount)
                
            if max_amount is not None:
                where_clauses.append("amount <= %s")
                params.append(max_amount)
                
            # Combine where clauses
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            # Add ordering, limit and offset
            query += " ORDER BY transaction_date DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            transactions_data = cursor.fetchall()
            
            transactions = []
            for txn_data in transactions_data:
                transaction = Transaction(
                    id=txn_data['id'],
                    account_id=txn_data['account_id'],
                    category_id=txn_data['category_id'],
                    amount=float(txn_data['amount']),
                    transaction_type=txn_data['transaction_type'],
                    description=txn_data['description'],
                    transaction_date=txn_data['transaction_date'],
                    created_by_user_id=txn_data['created_by_user_id'],
                    recipient_account_id=txn_data['recipient_account_id'],
                    external_recipient=txn_data['external_recipient']
                )
                
                # Add details if included
                if include_details:
                    transaction._account_name = txn_data['account_name']
                    transaction._category_name = txn_data.get('category_name')
                    transaction._recipient_account_name = txn_data.get('recipient_account_name')
                    transaction._created_by_name = txn_data['created_by_name']
                    
                transactions.append(transaction)
            
            return transactions
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_transactions_for_user(user_id, limit=100, offset=0, start_date=None, end_date=None,
                                  category_id=None, search_term=None, transaction_type=None,
                                  min_amount=None, max_amount=None, account_id=None, include_details=False):
        """Get all transactions for a user's accounts with filtering options."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get all account IDs for the user
            if account_id is None:
                account_query = """
                SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
                """
                cursor.execute(account_query, (user_id,))
                account_ids = [row['id'] for row in cursor.fetchall()]
                
                if not account_ids:
                    return []
            else:
                account_ids = [account_id]
                
            # Base query
            if include_details:
                query = """
                SELECT t.id, t.account_id, t.category_id, t.amount, t.transaction_type, t.description, 
                       t.transaction_date, t.created_by_user_id, t.recipient_account_id, t.external_recipient,
                       a.account_name, 
                       tc.category_name, tc.is_expense, tc.icon, tc.color,
                       ra.account_name as recipient_account_name,
                       CONCAT(u.first_name, ' ', u.last_name) as created_by_name
                FROM transactions t
                LEFT JOIN accounts a ON t.account_id = a.id
                LEFT JOIN transaction_categories tc ON t.category_id = tc.id
                LEFT JOIN accounts ra ON t.recipient_account_id = ra.id
                LEFT JOIN users u ON t.created_by_user_id = u.id
                """
            else:
                query = """
                SELECT id, account_id, category_id, amount, transaction_type, description, 
                       transaction_date, created_by_user_id, recipient_account_id, external_recipient
                FROM transactions
                """
                
            # Build where clause for account IDs
            account_placeholders = ", ".join(["%s"] * len(account_ids))
            where_clause = f"(account_id IN ({account_placeholders}) OR recipient_account_id IN ({account_placeholders}))"
            params = account_ids + account_ids  # Duplicate for both IN clauses
            
            # Add other filters
            if start_date:
                where_clause += " AND transaction_date >= %s"
                params.append(start_date)
                
            if end_date:
                where_clause += " AND transaction_date <= %s"
                params.append(end_date)
                
            if category_id:
                where_clause += " AND category_id = %s"
                params.append(category_id)
                
            if search_term:
                where_clause += " AND (description LIKE %s OR external_recipient LIKE %s)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
                
            if transaction_type:
                where_clause += " AND transaction_type = %s"
                params.append(transaction_type)
                
            if min_amount is not None:
                where_clause += " AND amount >= %s"
                params.append(min_amount)
                
            if max_amount is not None:
                where_clause += " AND amount <= %s"
                params.append(max_amount)
                
            # Add where clause to query
            query += f" WHERE {where_clause}"
                
            # Add ordering, limit and offset
            query += " ORDER BY transaction_date DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            transactions_data = cursor.fetchall()
            
            transactions = []
            for txn_data in transactions_data:
                transaction = Transaction(
                    id=txn_data['id'],
                    account_id=txn_data['account_id'],
                    category_id=txn_data['category_id'],
                    amount=float(txn_data['amount']),
                    transaction_type=txn_data['transaction_type'],
                    description=txn_data['description'],
                    transaction_date=txn_data['transaction_date'],
                    created_by_user_id=txn_data['created_by_user_id'],
                    recipient_account_id=txn_data['recipient_account_id'],
                    external_recipient=txn_data['external_recipient']
                )
                
                # Add details if included
                if include_details:
                    transaction._account_name = txn_data['account_name']
                    transaction._category_name = txn_data.get('category_name')
                    transaction._recipient_account_name = txn_data.get('recipient_account_name')
                    transaction._created_by_name = txn_data['created_by_name']
                    
                transactions.append(transaction)
            
            return transactions
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def get_category_spending(user_id, start_date=None, end_date=None, is_expense=True):
        """Get spending by category for a user within a date range."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get all account IDs for the user
            account_query = """
            SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
            """
            cursor.execute(account_query, (user_id,))
            account_ids = [row['id'] for row in cursor.fetchall()]
            
            if not account_ids:
                return []
                
            # Build query for category spending
            query = """
            SELECT tc.id as category_id, tc.category_name, tc.icon, tc.color,
                   SUM(t.amount) as total_amount,
                   COUNT(t.id) as transaction_count
            FROM transactions t
            JOIN transaction_categories tc ON t.category_id = tc.id
            WHERE t.account_id IN ({}) AND tc.is_expense = %s
            """.format(", ".join(["%s"] * len(account_ids)))
            
            params = account_ids + [is_expense]
            
            # Add date filters if provided
            if start_date:
                query += " AND t.transaction_date >= %s"
                params.append(start_date)
                
            if end_date:
                query += " AND t.transaction_date <= %s"
                params.append(end_date)
                
            # Group by category and order by total amount
            query += " GROUP BY tc.id, tc.category_name, tc.icon, tc.color ORDER BY total_amount DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def search_transactions(user_id, search_term, limit=50):
        """Search for transactions by description, category, or amount."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get all account IDs for the user
            account_query = """
            SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
            """
            cursor.execute(account_query, (user_id,))
            account_ids = [row['id'] for row in cursor.fetchall()]
            
            if not account_ids:
                return []
                
            # Build query for searching transactions
            query = """
            SELECT t.id, t.account_id, t.category_id, t.amount, t.transaction_type, t.description, 
                   t.transaction_date, t.created_by_user_id, t.recipient_account_id, t.external_recipient,
                   a.account_name, 
                   tc.category_name, tc.is_expense,
                   ra.account_name as recipient_account_name
            FROM transactions t
            LEFT JOIN accounts a ON t.account_id = a.id
            LEFT JOIN transaction_categories tc ON t.category_id = tc.id
            LEFT JOIN accounts ra ON t.recipient_account_id = ra.id
            WHERE t.account_id IN ({}) AND (
                t.description LIKE %s OR 
                tc.category_name LIKE %s OR 
                t.external_recipient LIKE %s OR
                CAST(t.amount AS CHAR) LIKE %s
            )
            """.format(", ".join(["%s"] * len(account_ids)))
            
            search_pattern = f"%{search_term}%"
            params = account_ids + [search_pattern, search_pattern, search_pattern, search_pattern]
            
            # Add ordering and limit
            query += " ORDER BY t.transaction_date DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            transactions_data = cursor.fetchall()
            
            transactions = []
            for txn_data in transactions_data:
                transaction = Transaction(
                    id=txn_data['id'],
                    account_id=txn_data['account_id'],
                    category_id=txn_data['category_id'],
                    amount=float(txn_data['amount']),
                    transaction_type=txn_data['transaction_type'],
                    description=txn_data['description'],
                    transaction_date=txn_data['transaction_date'],
                    created_by_user_id=txn_data['created_by_user_id'],
                    recipient_account_id=txn_data['recipient_account_id'],
                    external_recipient=txn_data['external_recipient']
                )
                
                # Add cached data
                transaction._account_name = txn_data['account_name']
                transaction._category_name = txn_data.get('category_name')
                transaction._recipient_account_name = txn_data.get('recipient_account_name')
                
                transactions.append(transaction)
            
            return transactions
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_transaction_count(user_id, start_date=None, end_date=None):
        """Get the total number of transactions for a user."""
        connection = get_connection()
        if not connection:
            return 0

        try:
            cursor = connection.cursor()
            
            # Get all account IDs for the user
            account_query = """
            SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
            """
            cursor.execute(account_query, (user_id,))
            account_ids = [row['id'] for row in cursor.fetchall()]
            
            if not account_ids:
                return 0
                
            # Build query to count transactions
            query = """
            SELECT COUNT(*) FROM transactions 
            WHERE account_id IN ({})
            """.format(", ".join(["%s"] * len(account_ids)))
            
            params = account_ids
            
            # Add date filters if provided
            if start_date:
                query += " AND transaction_date >= %s"
                params.append(start_date)
                
            if end_date:
                query += " AND transaction_date <= %s"
                params.append(end_date)
            
            cursor.execute(query, params)
            return cursor.fetchone()[0]
            
        except Error as e:
            print(f"Error: {e}")
            return 0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_transactions_report(user_id, start_date, end_date, account_id=None, category_id=None, transaction_type=None):
        """Get a report of transactions for a specific date range with optional filters."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get account IDs for the user
            if account_id:
                account_ids = [account_id]
            else:
                account_query = """
                SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
                """
                cursor.execute(account_query, (user_id,))
                account_ids = [row['id'] for row in cursor.fetchall()]
            
            if not account_ids:
                return []
                
            # Build detailed report query
            query = """
            SELECT t.id, t.account_id, t.category_id, t.amount, t.transaction_type, t.description, 
                   t.transaction_date, t.external_recipient,
                   a.account_name, 
                   tc.category_name, tc.is_expense,
                   ra.account_name as recipient_account_name,
                   CONCAT(u.first_name, ' ', u.last_name) as created_by_name
            FROM transactions t
            LEFT JOIN accounts a ON t.account_id = a.id
            LEFT JOIN transaction_categories tc ON t.category_id = tc.id
            LEFT JOIN accounts ra ON t.recipient_account_id = ra.id
            LEFT JOIN users u ON t.created_by_user_id = u.id
            WHERE t.account_id IN ({}) 
                  AND t.transaction_date BETWEEN %s AND %s
            """.format(", ".join(["%s"] * len(account_ids)))
            
            params = account_ids + [start_date, end_date]
            
            # Add optional filters
            if category_id:
                query += " AND t.category_id = %s"
                params.append(category_id)
                
            if transaction_type:
                query += " AND t.transaction_type = %s"
                params.append(transaction_type)
                
            # Order by date
            query += " ORDER BY t.transaction_date DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_monthly_summary(user_id, year=None):
        """Get monthly income and expense summary for a user."""
        if not year:
            year = datetime.now().year
            
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get all account IDs for the user
            account_query = """
            SELECT id FROM accounts WHERE user_id = %s AND is_active = TRUE
            """
            cursor.execute(account_query, (user_id,))
            account_ids = [row['id'] for row in cursor.fetchall()]
            
            if not account_ids:
                return []
                
            # Build query for monthly summary
            query = """
            SELECT 
                MONTH(t.transaction_date) as month,
                SUM(CASE WHEN tc.is_expense = 0 THEN t.amount ELSE 0 END) as income,
                SUM(CASE WHEN tc.is_expense = 1 THEN t.amount ELSE 0 END) as expenses
            FROM transactions t
            JOIN transaction_categories tc ON t.category_id = tc.id
            WHERE t.account_id IN ({}) 
                  AND YEAR(t.transaction_date) = %s
            GROUP BY MONTH(t.transaction_date)
            ORDER BY month
            """.format(", ".join(["%s"] * len(account_ids)))
            
            params = account_ids + [year]
            
            cursor.execute(query, params)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    # Helper properties for cached data
    @property
    def account_name(self):
        """Get the account name (cached or from DB)."""
        if self._account_name is None and self.account_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT account_name FROM accounts WHERE id = %s", (self.account_id,))
                    result = cursor.fetchone()
                    if result:
                        self._account_name = result['account_name']
                except Error as e:
                    print(f"Error getting account name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._account_name

    @property
    def category_name(self):
        """Get the category name (cached or from DB)."""
        if self._category_name is None and self.category_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT category_name FROM transaction_categories WHERE id = %s", (self.category_id,))
                    result = cursor.fetchone()
                    if result:
                        self._category_name = result['category_name']
                except Error as e:
                    print(f"Error getting category name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._category_name

    @property
    def recipient_account_name(self):
        """Get the recipient account name (cached or from DB)."""
        if self._recipient_account_name is None and self.recipient_account_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT account_name FROM accounts WHERE id = %s", (self.recipient_account_id,))
                    result = cursor.fetchone()
                    if result:
                        self._recipient_account_name = result['account_name']
                except Error as e:
                    print(f"Error getting recipient account name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._recipient_account_name

    @property
    def created_by_name(self):
        """Get the name of the user who created the transaction (cached or from DB)."""
        if self._created_by_name is None and self.created_by_user_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute(
                        "SELECT CONCAT(first_name, ' ', last_name) as full_name FROM users WHERE id = %s", 
                        (self.created_by_user_id,)
                    )
                    result = cursor.fetchone()
                    if result:
                        self._created_by_name = result['full_name']
                except Error as e:
                    print(f"Error getting creator name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._created_by_name 