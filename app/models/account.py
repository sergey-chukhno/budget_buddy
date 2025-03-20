import mysql.connector
from mysql.connector import Error
import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_setup import get_connection

class Account:
    def __init__(self, id=None, user_id=None, account_type_id=None, account_name=None, balance=0.0, created_at=None, is_active=True):
        self.id = id
        self.user_id = user_id
        self.account_type_id = account_type_id
        self.account_name = account_name
        self.balance = balance
        self.created_at = created_at
        self.is_active = is_active
        self._account_type_name = None  # For caching

    @property
    def account_type_name(self):
        """Get the account type name."""
        if self._account_type_name is None and self.account_type_id is not None:
            connection = get_connection()
            if connection:
                try:
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT type_name FROM account_types WHERE id = %s", (self.account_type_id,))
                    result = cursor.fetchone()
                    if result:
                        self._account_type_name = result['type_name']
                except Error as e:
                    print(f"Error getting account type name: {e}")
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
        return self._account_type_name

    @staticmethod
    def create(user_id, account_type_id, account_name, initial_balance=0.0):
        """Create a new account."""
        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Check if account name already exists for this user
            cursor.execute("SELECT id FROM accounts WHERE user_id = %s AND account_name = %s", (user_id, account_name))
            if cursor.fetchone():
                return False, "Account name already exists for this user"
            
            # Create the account
            query = """
            INSERT INTO accounts (user_id, account_type_id, account_name, balance)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, account_type_id, account_name, initial_balance))
            connection.commit()
            
            # Get the account id
            account_id = cursor.lastrowid
            
            # Create a transaction record for the initial balance if > 0
            if initial_balance > 0:
                # Get the user for created_by field
                transaction_query = """
                INSERT INTO transactions (account_id, amount, transaction_type, description, created_by_user_id)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(transaction_query, (account_id, initial_balance, 'deposit', 'Initial deposit', user_id))
                connection.commit()
            
            return True, account_id
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_by_id(account_id):
        """Get an account by ID."""
        connection = get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, user_id, account_type_id, account_name, balance, created_at, is_active
            FROM accounts
            WHERE id = %s
            """
            cursor.execute(query, (account_id,))
            account_data = cursor.fetchone()
            
            if not account_data:
                return None
            
            return Account(
                id=account_data['id'],
                user_id=account_data['user_id'],
                account_type_id=account_data['account_type_id'],
                account_name=account_data['account_name'],
                balance=float(account_data['balance']),
                created_at=account_data['created_at'],
                is_active=account_data['is_active']
            )
            
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_accounts_for_user(user_id, include_inactive=False):
        """Get all accounts for a user."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT a.id, a.user_id, a.account_type_id, a.account_name, a.balance, a.created_at, a.is_active, at.type_name
            FROM accounts a
            JOIN account_types at ON a.account_type_id = at.id
            WHERE a.user_id = %s
            """
            
            if not include_inactive:
                query += " AND a.is_active = TRUE"
                
            cursor.execute(query, (user_id,))
            accounts_data = cursor.fetchall()
            
            accounts = []
            for account_data in accounts_data:
                account = Account(
                    id=account_data['id'],
                    user_id=account_data['user_id'],
                    account_type_id=account_data['account_type_id'],
                    account_name=account_data['account_name'],
                    balance=float(account_data['balance']),
                    created_at=account_data['created_at'],
                    is_active=account_data['is_active']
                )
                account._account_type_name = account_data['type_name']  # Set the cached type name
                accounts.append(account)
            
            return accounts
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self, account_name=None, is_active=None):
        """Update account information."""
        if not self.id:
            return False, "Account ID not set"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Update only the fields that are provided
            updates = []
            params = []
            
            if account_name is not None:
                # Check if name already exists for this user
                cursor.execute(
                    "SELECT id FROM accounts WHERE user_id = %s AND account_name = %s AND id != %s", 
                    (self.user_id, account_name, self.id)
                )
                if cursor.fetchone():
                    return False, "Account name already exists for this user"
                    
                updates.append("account_name = %s")
                params.append(account_name)
                self.account_name = account_name
                
            if is_active is not None:
                updates.append("is_active = %s")
                params.append(is_active)
                self.is_active = is_active
                
            if not updates:
                return True, "No updates provided"
                
            # Add the account ID to the parameters
            params.append(self.id)
            
            # Create and execute the update query
            query = f"""
            UPDATE accounts
            SET {', '.join(updates)}
            WHERE id = %s
            """
            cursor.execute(query, params)
            connection.commit()
            
            return True, "Account updated successfully"
            
        except Error as e:
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_funds(self, amount, category_id, description, created_by_user_id):
        """Add funds to the account."""
        if not self.id:
            return False, "Account ID not set"
            
        if amount <= 0:
            return False, "Amount must be positive"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Start a transaction
            connection.start_transaction()
            
            # Update the account balance
            update_query = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
            """
            cursor.execute(update_query, (amount, self.id))
            
            # Create a transaction record
            transaction_query = """
            INSERT INTO transactions (account_id, category_id, amount, transaction_type, description, created_by_user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                transaction_query, 
                (self.id, category_id, amount, 'deposit', description, created_by_user_id)
            )
            
            # Get the transaction id
            transaction_id = cursor.lastrowid
            
            # Create an audit log entry
            audit_query = """
            INSERT INTO transaction_audit_log (transaction_id, user_id, action, details)
            VALUES (%s, %s, %s, %s)
            """
            audit_details = f"Added {amount} to account {self.account_name} (ID: {self.id})"
            cursor.execute(audit_query, (transaction_id, created_by_user_id, 'deposit', audit_details))
            
            # Commit the transaction
            connection.commit()
            
            # Update the balance in memory
            self.balance += amount
            
            return True, transaction_id
            
        except Error as e:
            connection.rollback()
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def withdraw_funds(self, amount, category_id, description, created_by_user_id):
        """Withdraw funds from the account."""
        if not self.id:
            return False, "Account ID not set"
            
        if amount <= 0:
            return False, "Amount must be positive"
            
        if amount > self.balance:
            return False, "Insufficient funds"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Start a transaction
            connection.start_transaction()
            
            # Update the account balance
            update_query = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s
            """
            cursor.execute(update_query, (amount, self.id))
            
            # Create a transaction record
            transaction_query = """
            INSERT INTO transactions (account_id, category_id, amount, transaction_type, description, created_by_user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                transaction_query, 
                (self.id, category_id, amount, 'withdrawal', description, created_by_user_id)
            )
            
            # Get the transaction id
            transaction_id = cursor.lastrowid
            
            # Create an audit log entry
            audit_query = """
            INSERT INTO transaction_audit_log (transaction_id, user_id, action, details)
            VALUES (%s, %s, %s, %s)
            """
            audit_details = f"Withdrew {amount} from account {self.account_name} (ID: {self.id})"
            cursor.execute(audit_query, (transaction_id, created_by_user_id, 'withdrawal', audit_details))
            
            # Commit the transaction
            connection.commit()
            
            # Update the balance in memory
            self.balance -= amount
            
            return True, transaction_id
            
        except Error as e:
            connection.rollback()
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def transfer_funds(source_account_id, target_account_id, amount, description, created_by_user_id):
        """Transfer funds between accounts."""
        if amount <= 0:
            return False, "Amount must be positive"

        # Get the source account
        source_account = Account.get_by_id(source_account_id)
        if not source_account:
            return False, "Source account not found"
            
        # Check if source account has sufficient funds
        if source_account.balance < amount:
            return False, "Insufficient funds in source account"
            
        # Get the target account
        target_account = Account.get_by_id(target_account_id)
        if not target_account:
            return False, "Target account not found"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Start a transaction
            connection.start_transaction()
            
            # Update the source account balance
            source_update_query = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s
            """
            cursor.execute(source_update_query, (amount, source_account_id))
            
            # Update the target account balance
            target_update_query = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
            """
            cursor.execute(target_update_query, (amount, target_account_id))
            
            # Create a transaction record
            transaction_query = """
            INSERT INTO transactions (account_id, amount, transaction_type, description, created_by_user_id, recipient_account_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                transaction_query, 
                (source_account_id, amount, 'transfer', description, created_by_user_id, target_account_id)
            )
            
            # Get the transaction id
            transaction_id = cursor.lastrowid
            
            # Create an audit log entry
            audit_query = """
            INSERT INTO transaction_audit_log (transaction_id, user_id, action, details)
            VALUES (%s, %s, %s, %s)
            """
            audit_details = f"Transferred {amount} from account {source_account.account_name} (ID: {source_account_id}) to account {target_account.account_name} (ID: {target_account_id})"
            cursor.execute(audit_query, (transaction_id, created_by_user_id, 'transfer', audit_details))
            
            # Commit the transaction
            connection.commit()
            
            return True, transaction_id
            
        except Error as e:
            connection.rollback()
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def send_external(self, amount, category_id, external_recipient, description, created_by_user_id):
        """Send funds to an external account."""
        if not self.id:
            return False, "Account ID not set"
            
        if amount <= 0:
            return False, "Amount must be positive"
            
        if amount > self.balance:
            return False, "Insufficient funds"

        connection = get_connection()
        if not connection:
            return False, "Database connection error"

        try:
            cursor = connection.cursor()
            
            # Start a transaction
            connection.start_transaction()
            
            # Update the account balance
            update_query = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s
            """
            cursor.execute(update_query, (amount, self.id))
            
            # Create a transaction record
            transaction_query = """
            INSERT INTO transactions (account_id, category_id, amount, transaction_type, description, created_by_user_id, external_recipient)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                transaction_query, 
                (self.id, category_id, amount, 'external_transfer', description, created_by_user_id, external_recipient)
            )
            
            # Get the transaction id
            transaction_id = cursor.lastrowid
            
            # Create an audit log entry
            audit_query = """
            INSERT INTO transaction_audit_log (transaction_id, user_id, action, details)
            VALUES (%s, %s, %s, %s)
            """
            audit_details = f"Sent {amount} from account {self.account_name} (ID: {self.id}) to external recipient: {external_recipient}"
            cursor.execute(audit_query, (transaction_id, created_by_user_id, 'external_transfer', audit_details))
            
            # Commit the transaction
            connection.commit()
            
            # Update the balance in memory
            self.balance -= amount
            
            return True, transaction_id
            
        except Error as e:
            connection.rollback()
            return False, f"Database error: {e}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_account_types():
        """Get all account types."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT id, type_name, description FROM account_types")
            return cursor.fetchall()
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_total_balance_for_user(user_id):
        """Get the total balance across all accounts for a user."""
        connection = get_connection()
        if not connection:
            return 0.0

        try:
            cursor = connection.cursor()
            
            query = """
            SELECT SUM(balance) 
            FROM accounts 
            WHERE user_id = %s AND is_active = TRUE
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()[0]
            
            return float(result) if result is not None else 0.0
            
        except Error as e:
            print(f"Error: {e}")
            return 0.0
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_balance_history(account_id, start_date=None, end_date=None):
        """Get the balance history for an account."""
        connection = get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            
            # Construct the query based on date parameters
            query = """
            SELECT transaction_date, 
                   SUM(CASE 
                       WHEN transaction_type = 'deposit' THEN amount 
                       WHEN transaction_type IN ('withdrawal', 'transfer', 'external_transfer') AND account_id = %s THEN -amount 
                       WHEN transaction_type = 'transfer' AND recipient_account_id = %s THEN amount 
                       ELSE 0 
                   END) as daily_change,
                   DATE(transaction_date) as date
            FROM transactions
            WHERE (account_id = %s OR recipient_account_id = %s)
            """
            
            params = [account_id, account_id, account_id, account_id]
            
            if start_date:
                query += " AND transaction_date >= %s"
                params.append(start_date)
                
            if end_date:
                query += " AND transaction_date <= %s"
                params.append(end_date)
                
            query += " GROUP BY DATE(transaction_date) ORDER BY transaction_date"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Get the initial balance before the start date
            initial_balance_query = """
            SELECT balance - COALESCE(
                (SELECT SUM(CASE 
                    WHEN transaction_type = 'deposit' THEN amount 
                    WHEN transaction_type IN ('withdrawal', 'transfer', 'external_transfer') AND account_id = %s THEN -amount 
                    WHEN transaction_type = 'transfer' AND recipient_account_id = %s THEN amount 
                    ELSE 0 
                END)
                FROM transactions
                WHERE (account_id = %s OR recipient_account_id = %s)
                """
            
            initial_params = [account_id, account_id, account_id, account_id]
            
            if start_date:
                initial_balance_query += " AND transaction_date >= %s"
                initial_params.append(start_date)
                
            initial_balance_query += "), 0) as initial_balance FROM accounts WHERE id = %s"
            initial_params.append(account_id)
            
            cursor.execute(initial_balance_query, initial_params)
            initial_balance = cursor.fetchone()['initial_balance']
            
            # Calculate the running balance
            balance_history = []
            running_balance = float(initial_balance)
            
            for row in results:
                running_balance += float(row['daily_change'])
                balance_history.append({
                    'date': row['date'],
                    'balance': running_balance
                })
            
            return balance_history
            
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 