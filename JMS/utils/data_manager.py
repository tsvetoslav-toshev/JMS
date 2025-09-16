import json
import csv
import shutil
from datetime import datetime, date
from pathlib import Path
import sqlite3
import logging
from typing import List, Dict, Any
import os

class DataManager:
    def __init__(self, database_or_path, backup_dir="backups", audit_log="logs/audit.log"):
        """Initialize DataManager with either a Database object or database path"""
        # Handle both Database object and string path
        if hasattr(database_or_path, 'db_path'):  # It's a Database object
            self.database = database_or_path
            self.db_path = Path(database_or_path.db_path)
        else:  # It's a string path
            self.database = None
            self.db_path = Path(database_or_path)
            
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
        self.setup_logging(audit_log)

    def export_data(self, output_path: str, format_type: str = "json") -> bool:
        """Export database data to file - updated method signature"""
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"exports/export_{timestamp}.{format_type}"
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use the database object if available, otherwise connect directly
            if self.database:
                data = self._export_via_database_object()
            else:
                data = self._export_via_direct_connection()

            if format_type.lower() == "json":
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            elif format_type.lower() == "csv":
                # For CSV, create a combined file with all tables
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Write header
                    writer.writerow(["Table", "Data"])
                    
                    # Write each table's data
                    for table_name, table_data in data.items():
                        writer.writerow([f"=== {table_name} ===", ""])
                        if table_data["rows"]:
                            # Write column headers
                            writer.writerow(table_data["columns"])
                            # Write data rows
                            for row_dict in table_data["rows"]:
                                row_values = [row_dict.get(col, "") for col in table_data["columns"]]
                                writer.writerow(row_values)
                        writer.writerow(["", ""])  # Empty row separator

            self.audit_logger.info(f"Data exported to: {output_path}")
            return True
        except Exception as e:
            self.audit_logger.error(f"Export failed: {str(e)}")
            return False

    def _export_via_database_object(self):
        """Export data using the Database object"""
        data = {}
        
        # Export items
        items = self.database.get_all_items()
        if items:
            columns = ["id", "barcode", "name", "description", "category", "price", "cost", 
                      "weight", "metal_type", "stone_type", "stock_quantity", "created_at", "updated_at"]
            data["items"] = {
                "columns": columns,
                "rows": [dict(zip(columns, item)) for item in items]
            }
        
        # Export shops
        shops = self.database.get_all_shops()
        if shops:
            columns = ["id", "name", "created_at"]
            data["shops"] = {
                "columns": columns,
                "rows": [dict(zip(columns, shop)) for shop in shops]
            }
        
        return data

    def _export_via_direct_connection(self):
        """Export data using direct database connection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        data = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            data[table_name] = {
                "columns": columns,
                "rows": [dict(zip(columns, row)) for row in rows]
            }
        
        conn.close()
        return data

    def setup_logging(self, audit_log: str):
        """Setup audit logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        self.audit_logger = logging.getLogger('audit')
        self.audit_logger.setLevel(logging.INFO)
        handler = logging.FileHandler(audit_log)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)

    def create_backup(self) -> str:
        """Create a backup of the database"""
        try:
            # Use Bulgarian format matching export files: резервно_копие - DD.MM.YYYY_HH.MM.SS.db
            # Note: Using dots instead of colons for Windows compatibility
            now = datetime.now()
            date_str = now.strftime("%d.%m.%Y")
            time_str = now.strftime("%H.%M.%S")  # Use dots instead of colons
            backup_filename = f"резервно_копие - {date_str}_{time_str}.db"
            
            backup_path = self.backup_dir / backup_filename
            
            # Create backup
            shutil.copy2(self.db_path, backup_path)
            
            self.audit_logger.info(f"Database backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            self.audit_logger.error(f"Backup failed: {str(e)}")
            raise

    def restore_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                raise FileNotFoundError("Backup file not found")

            # Create a backup of current database before restore
            self.create_backup()
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            self.audit_logger.info(f"Database restored from backup: {backup_path}")
            return True
        except Exception as e:
            self.audit_logger.error(f"Restore failed: {str(e)}")
            return False

    def import_data(self, import_path: str, format: str = "json") -> bool:
        """Import data from file to database"""
        try:
            import_path = Path(import_path)
            if not import_path.exists():
                raise FileNotFoundError("Import file not found")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if format.lower() == "json":
                with open(import_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for table_name, table_data in data.items():
                    # Clear existing data
                    cursor.execute(f"DELETE FROM {table_name}")
                    
                    # Insert new data
                    columns = table_data["columns"]
                    placeholders = ", ".join(["?" for _ in columns])
                    for row in table_data["rows"]:
                        values = [row[col] for col in columns]
                        cursor.execute(
                            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})",
                            values
                        )

            elif format.lower() == "csv":
                # Handle CSV import for each table
                for csv_file in import_path.parent.glob(f"*_{import_path.name}"):
                    table_name = csv_file.stem.split('_')[0]
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        columns = reader.fieldnames
                        
                        # Create table if it doesn't exist
                        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")
                        
                        # Insert data
                        for row in reader:
                            values = [row[col] for col in columns]
                            placeholders = ', '.join(['?'] * len(columns))
                            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

            conn.commit()
            self.audit_logger.info(f"Data imported from: {import_path}")
            return True
        except Exception as e:
            self.audit_logger.error(f"Import failed: {str(e)}")
            return False
        finally:
            conn.close()

    def validate_data(self, data: Dict[str, Any], table_name: str) -> List[str]:
        """Validate data before import"""
        errors = []
        
        # Validate required fields
        required_fields = {
            "items": ["sku", "name", "category", "price", "cost"],
            "sales": ["item_id", "quantity", "sale_price"],
            "branches": ["name", "address"]
        }
        
        for field in required_fields.get(table_name, []):
            if field not in data or not data[field]:
                errors.append(f"Missing required field '{field}' in {table_name}")
        
        # Validate data types
        for field, value in data.items():
            if field in required_fields[table_name]:
                if isinstance(value, (int, float)):
                    if field == "price" and not isinstance(value, (int, float)):
                        errors.append(f"Invalid price type in {table_name}")
                    elif field == "cost" and not isinstance(value, (int, float)):
                        errors.append(f"Invalid cost type in {table_name}")
                    elif field == "stock_quantity" and not isinstance(value, int):
                        errors.append(f"Invalid stock quantity type in {table_name}")
                elif isinstance(value, str):
                    if field == "name" and not value.isalpha():
                        errors.append(f"Invalid name format in {table_name}")
                    elif field == "category" and not value.isalpha():
                        errors.append(f"Invalid category format in {table_name}")
                elif isinstance(value, (datetime, date)):
                    if field == "sale_date":
                        errors.append(f"Invalid sale_date format in {table_name}")
                elif isinstance(value, dict):
                    if field == "address" and not self.validate_data(value, "branches"):
                        errors.append(f"Invalid address format in {table_name}")
                elif isinstance(value, list):
                    if field == "items" and not self.validate_data(value, "items"):
                        errors.append(f"Invalid items format in {table_name}")
        
        return errors

    def sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data before import"""
        sanitized = {}
        
        for table_name, table_data in data.items():
            sanitized[table_name] = {
                "columns": table_data["columns"],
                "rows": []
            }
            
            for row in table_data["rows"]:
                sanitized_row = {}
                for key, value in row.items():
                    # Remove leading/trailing whitespace
                    if isinstance(value, str):
                        value = value.strip()
                    
                    # Convert empty strings to None
                    if value == "":
                        value = None
                    
                    # Round numeric values
                    if isinstance(value, float):
                        value = round(value, 2)
                    
                    sanitized_row[key] = value
                
                sanitized[table_name]["rows"].append(sanitized_row)
        
        return sanitized 