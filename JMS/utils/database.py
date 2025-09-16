from pathlib import Path
import sqlite3
import logging
from datetime import datetime
from .data_manager import DataManager

class Database:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.data_manager = DataManager(str(db_path))
        self.setup_logging()
        self.initialize_database()

    def setup_logging(self):
        """Setup logging for database operations"""
        self.logger = logging.getLogger('database')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('logs/database.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_operation(self, operation: str, details: str):
        """Log database operations"""
        self.logger.info(f"{operation}: {details}")

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        """Initialize database tables"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create inventory table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER NOT NULL,
                        branch_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (branch_id) REFERENCES branches (id)
                    )
                ''')

                # Create sales table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        total_price REAL NOT NULL,
                        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        branch_id INTEGER NOT NULL,
                        FOREIGN KEY (item_id) REFERENCES inventory (id),
                        FOREIGN KEY (branch_id) REFERENCES branches (id)
                    )
                ''')

                # Create branches table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS branches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        address TEXT NOT NULL,
                        phone TEXT,
                        email TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Create audit_log table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation TEXT NOT NULL,
                        table_name TEXT NOT NULL,
                        record_id INTEGER,
                        details TEXT,
                        user TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                conn.commit()
                self.log_operation("INITIALIZE", "Database tables created successfully")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            raise

    def add_inventory_item(self, name: str, description: str, category: str, price: float, quantity: int, branch_id: int):
        """Add new inventory item with validation"""
        try:
            # Validate data
            data = {
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "quantity": quantity,
                "branch_id": branch_id
            }
            self.data_manager.validate_data(data, "inventory")
            
            # Sanitize data
            sanitized_data = self.data_manager.sanitize_data(data)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO inventory (name, description, category, price, quantity, branch_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    sanitized_data["name"],
                    sanitized_data["description"],
                    sanitized_data["category"],
                    sanitized_data["price"],
                    sanitized_data["quantity"],
                    sanitized_data["branch_id"]
                ))
                
                item_id = cursor.lastrowid
                self.log_operation("INSERT", f"Added inventory item: {name} (ID: {item_id})")
                return item_id
        except Exception as e:
            self.logger.error(f"Failed to add inventory item: {str(e)}")
            raise

    def update_inventory_item(self, item_id: int, **kwargs):
        """Update inventory item with validation"""
        try:
            # Validate data
            self.data_manager.validate_data(kwargs, "inventory")
            
            # Sanitize data
            sanitized_data = self.data_manager.sanitize_data(kwargs)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                set_clause = ", ".join([f"{k} = ?" for k in sanitized_data.keys()])
                query = f"UPDATE inventory SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                
                cursor.execute(query, list(sanitized_data.values()) + [item_id])
                self.log_operation("UPDATE", f"Updated inventory item ID: {item_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to update inventory item: {str(e)}")
            raise

    def delete_inventory_item(self, item_id: int):
        """Delete inventory item with logging"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
                self.log_operation("DELETE", f"Deleted inventory item ID: {item_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to delete inventory item: {str(e)}")
            raise

    def add_sale(self, item_id: int, quantity: int, total_price: float, branch_id: int):
        """Add new sale with validation"""
        try:
            # Validate data
            data = {
                "item_id": item_id,
                "quantity": quantity,
                "total_price": total_price,
                "branch_id": branch_id
            }
            self.data_manager.validate_data(data, "sales")
            
            # Sanitize data
            sanitized_data = self.data_manager.sanitize_data(data)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sales (item_id, quantity, total_price, branch_id)
                    VALUES (?, ?, ?, ?)
                ''', (
                    sanitized_data["item_id"],
                    sanitized_data["quantity"],
                    sanitized_data["total_price"],
                    sanitized_data["branch_id"]
                ))
                
                sale_id = cursor.lastrowid
                self.log_operation("INSERT", f"Added sale ID: {sale_id}")
                return sale_id
        except Exception as e:
            self.logger.error(f"Failed to add sale: {str(e)}")
            raise

    def add_branch(self, name: str, address: str, phone: str = None, email: str = None):
        """Add new branch with validation"""
        try:
            # Validate data
            data = {
                "name": name,
                "address": address,
                "phone": phone,
                "email": email
            }
            self.data_manager.validate_data(data, "branches")
            
            # Sanitize data
            sanitized_data = self.data_manager.sanitize_data(data)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO branches (name, address, phone, email)
                    VALUES (?, ?, ?, ?)
                ''', (
                    sanitized_data["name"],
                    sanitized_data["address"],
                    sanitized_data["phone"],
                    sanitized_data["email"]
                ))
                
                branch_id = cursor.lastrowid
                self.log_operation("INSERT", f"Added branch: {name} (ID: {branch_id})")
                return branch_id
        except Exception as e:
            self.logger.error(f"Failed to add branch: {str(e)}")
            raise

    def update_branch(self, branch_id: int, **kwargs):
        """Update branch with validation"""
        try:
            # Validate data
            self.data_manager.validate_data(kwargs, "branches")
            
            # Sanitize data
            sanitized_data = self.data_manager.sanitize_data(kwargs)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                set_clause = ", ".join([f"{k} = ?" for k in sanitized_data.keys()])
                query = f"UPDATE branches SET {set_clause} WHERE id = ?"
                
                cursor.execute(query, list(sanitized_data.values()) + [branch_id])
                self.log_operation("UPDATE", f"Updated branch ID: {branch_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to update branch: {str(e)}")
            raise

    def delete_branch(self, branch_id: int):
        """Delete branch with logging"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM branches WHERE id = ?", (branch_id,))
                self.log_operation("DELETE", f"Deleted branch ID: {branch_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to delete branch: {str(e)}")
            raise

    def get_audit_log(self, start_date: str = None, end_date: str = None, operation: str = None):
        """Get audit log entries with optional filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM audit_log WHERE 1=1"
                params = []
                
                if start_date:
                    query += " AND timestamp >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND timestamp <= ?"
                    params.append(end_date)
                if operation:
                    query += " AND operation = ?"
                    params.append(operation)
                
                query += " ORDER BY timestamp DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Failed to get audit log: {str(e)}")
            raise 