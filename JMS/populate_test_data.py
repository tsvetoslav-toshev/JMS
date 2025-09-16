#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Data Population Script for Jewelry Management System

This script populates the database with realistic test data that follows
the correct warehouse-centric inventory model:

WAREHOUSE (items.stock_quantity) → SHOPS (shop_items.quantity) → SALES

DO NOT modify the main application - this is just for testing!
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

def populate_test_data():
    """Populate database with realistic test data following correct architecture"""
    try:
        # Connect to database
        db_path = os.path.join("data", "jewelry.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Starting test data population...")
        
        # 1. CREATE TEST SHOPS
        test_shops = [
            "Магазин Център",
            "Магазин Мол", 
            "Магазин Пешеходна"
        ]
        
        for shop_name in test_shops:
            cursor.execute("INSERT OR IGNORE INTO shops (name) VALUES (?)", (shop_name,))
        
        print("✅ Test shops created")
        
        # 2. CREATE TEST ITEMS (in warehouse only - no shop_id column!)
        test_items = [
            # Rings
            ("1000001", "Златен пръстен с диамант", "Пръстен с 0.5ct диамант", "Пръстени", 2500.00, 1800.00, 3.5, "Злато 18K", "Диамант", 15),
            ("1000002", "Сребърен пръстен", "Елегантен сребърен пръстен", "Пръстени", 150.00, 90.00, 2.8, "Сребро 925", "Няма", 25),
            ("1000003", "Пръстен с рубин", "Класически пръстен с рубин", "Пръстени", 1800.00, 1200.00, 4.2, "Злато 14K", "Рубин", 8),
            ("1000004", "Пръстен с изумруд", "Елегантен пръстен с изумруд", "Пръстени", 2200.00, 1600.00, 3.8, "Злато 18K", "Изумруд", 6),
            ("1000005", "Сребърен пръстен с циркон", "Модерен пръстен с циркон", "Пръстени", 95.00, 55.00, 2.2, "Сребро 925", "Циркон", 35),
            
            # Necklaces  
            ("2000001", "Златна верижка", "Елегантна златна верижка 45см", "Колиета", 890.00, 650.00, 12.5, "Злато 14K", "Няма", 20),
            ("2000002", "Сребърно колие с перла", "Колие с естествена перла", "Колиета", 320.00, 180.00, 8.3, "Сребро 925", "Перла", 12),
            ("2000003", "Верижка с висулка", "Златна верижка с диамантена висулка", "Колиета", 1500.00, 1100.00, 6.7, "Злато 18K", "Диамант", 6),
            ("2000004", "Сребърна верижка", "Класическа сребърна верижка", "Колиета", 180.00, 110.00, 8.9, "Сребро 925", "Няма", 28),
            ("2000005", "Колие с аметист", "Красиво колие с аметист", "Колиета", 450.00, 280.00, 5.4, "Сребро 925", "Аметист", 14),
            
            # Earrings
            ("3000001", "Златни обеци", "Класически златни обеци", "Обеци", 450.00, 300.00, 2.1, "Злато 14K", "Няма", 30),
            ("3000002", "Обеци с изумруд", "Обеци с естествен изумруд", "Обеци", 2200.00, 1600.00, 3.8, "Злато 18K", "Изумруд", 4),
            ("3000003", "Сребърни обеци", "Модерни сребърни обеци", "Обеци", 120.00, 75.00, 1.9, "Сребро 925", "Няма", 40),
            ("3000004", "Обеци с перли", "Елегантни обеци с перли", "Обеци", 280.00, 180.00, 2.5, "Сребро 925", "Перла", 22),
            ("3000005", "Златни обеци с циркон", "Блестящи обеци с циркон", "Обеци", 350.00, 220.00, 2.8, "Злато 14K", "Циркон", 18),
            
            # Bracelets
            ("4000001", "Златна гривна", "Елегантна златна гривна", "Гривни", 680.00, 480.00, 15.2, "Злато 14K", "Няма", 18),
            ("4000002", "Сребърна гривна с камъни", "Гривна с полускъпоценни камъни", "Гривни", 280.00, 160.00, 25.6, "Сребро 925", "Аметист", 22),
            ("4000003", "Златна гривна с диаманти", "Луксозна гривна с диаманти", "Гривни", 3200.00, 2400.00, 18.7, "Злато 18K", "Диамант", 3),
            ("4000004", "Сребърна гривна", "Класическа сребърна гривна", "Гривни", 150.00, 95.00, 22.3, "Сребро 925", "Няма", 25),
            
            # Watches
            ("5000001", "Златен часовник", "Луксозен златен часовник", "Часовници", 3500.00, 2800.00, 85.0, "Злато 18K", "Сафир", 3),
            ("5000002", "Сребърен часовник", "Елегантен сребърен часовник", "Часовници", 850.00, 600.00, 65.0, "Сребро 925", "Няма", 8),
            ("5000003", "Дамски златен часовник", "Фин дамски часовник", "Часовници", 1200.00, 900.00, 45.0, "Злато 14K", "Няма", 5),
            
            # Low stock items for testing
            ("6000001", "Ограничена серия пръстен", "Специален дизайнерски пръстен", "Пръстени", 5500.00, 4200.00, 4.8, "Платина", "Диамант", 2),
            ("6000002", "Антично колие", "Възстановено антично колие", "Колиета", 1800.00, 1200.00, 12.0, "Злато 14K", "Рубин", 1),
            ("6000003", "Ексклузивни обеци", "Ръчно изработени обеци", "Обеци", 980.00, 650.00, 3.2, "Сребро 925", "Танзанит", 3),
        ]
        
        for barcode, name, description, category, price, cost, weight, metal_type, stone_type, stock_qty in test_items:
            cursor.execute("""
                INSERT OR IGNORE INTO items 
                (barcode, name, description, category, price, cost, weight, metal_type, stone_type, stock_quantity) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (barcode, name, description, category, price, cost, weight, metal_type, stone_type, stock_qty))
        
        print("✅ Test items created in warehouse")
        
        # 3. DISTRIBUTE ITEMS TO SHOPS (simulate warehouse→shop transfers)
        cursor.execute("SELECT id, name FROM shops")
        shops = cursor.fetchall()
        
        cursor.execute("SELECT id, barcode, stock_quantity FROM items")
        items = cursor.fetchall()
        
        print("🔄 Distributing items to shops...")
        
        for item_id, barcode, warehouse_qty in items:
            if warehouse_qty <= 0:
                continue
                
            # Randomly distribute 50-80% of warehouse stock to shops
            total_to_distribute = int(warehouse_qty * random.uniform(0.5, 0.8))
            remaining_to_distribute = total_to_distribute
            
            for i, (shop_id, shop_name) in enumerate(shops):
                if remaining_to_distribute <= 0:
                    break
                    
                # Randomly decide if this shop gets this item (80% chance)
                if random.random() < 0.8:
                    # Last shop gets remaining quantity, others get random portion
                    if i == len(shops) - 1:
                        shop_qty = remaining_to_distribute
                    else:
                        max_for_shop = remaining_to_distribute // max(1, (len(shops) - i))
                        shop_qty = random.randint(1, max(1, max_for_shop))
                    
                    if shop_qty > 0:
                        # Add to shop_items
                        cursor.execute("""
                            INSERT OR REPLACE INTO shop_items 
                            (shop_id, item_id, quantity, created_at, updated_at) 
                            VALUES (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))
                        """, (shop_id, item_id, shop_qty))
                        
                        remaining_to_distribute -= shop_qty
            
            # Update warehouse stock (decrease by distributed amount)
            distributed_amount = total_to_distribute - remaining_to_distribute
            if distributed_amount > 0:
                cursor.execute("""
                    UPDATE items SET stock_quantity = stock_quantity - ?, updated_at = datetime('now', 'localtime') 
                    WHERE id = ?
                """, (distributed_amount, item_id))
        
        print("✅ Items distributed to shops")
        
        # 4. CREATE TEST SALES (from shop inventories only!)
        print("🔄 Creating test sales...")
        
        # Generate sales for last 45 days
        for days_ago in range(45):
            sale_date = datetime.now() - timedelta(days=days_ago)
            
            # Random number of sales per day (1-6)
            daily_sales = random.randint(1, 6)
            
            for _ in range(daily_sales):
                # Pick random shop that has inventory
                cursor.execute("""
                    SELECT si.shop_id, si.item_id, si.quantity, i.price, i.barcode, s.name
                    FROM shop_items si 
                    JOIN items i ON si.item_id = i.id 
                    JOIN shops s ON si.shop_id = s.id
                    WHERE si.quantity > 0
                """)
                available_items = cursor.fetchall()
                
                if available_items:
                    shop_id, item_id, available_qty, item_price, barcode, shop_name = random.choice(available_items)
                    
                    # Usually sell 1 item, sometimes 2
                    sale_qty = random.choices([1, 2], weights=[85, 15])[0]
                    sale_qty = min(sale_qty, available_qty)  # Don't oversell
                    
                    total_price = item_price * sale_qty
                    
                    # Add some time variation to sale_date
                    hours_offset = random.randint(9, 19)  # Business hours
                    minutes_offset = random.randint(0, 59)
                    sale_datetime = sale_date.replace(hour=hours_offset, minute=minutes_offset, second=0)
                    
                    # Record sale
                    cursor.execute("""
                        INSERT INTO sales (item_id, quantity, total_price, sale_date, shop_id) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (item_id, sale_qty, total_price, sale_datetime.strftime('%Y-%m-%d %H:%M:%S'), shop_id))
                    
                    # Decrease shop inventory (following the same logic as the app)
                    if available_qty == sale_qty:
                        cursor.execute("DELETE FROM shop_items WHERE shop_id = ? AND item_id = ?", 
                                     (shop_id, item_id))
                    else:
                        cursor.execute("""
                            UPDATE shop_items SET quantity = quantity - ?, updated_at = datetime('now', 'localtime') 
                            WHERE shop_id = ? AND item_id = ?
                        """, (sale_qty, shop_id, item_id))
        
        print("✅ Test sales created")
        
        # 5. CREATE SOME CUSTOM VALUES
        custom_categories = ["VIP Клиенти", "Сватбени колекции", "Мъжки бижута", "Детски бижута", "Винтидж колекция"]
        for category in custom_categories:
            cursor.execute("INSERT OR IGNORE INTO custom_values (type, value) VALUES (?, ?)", 
                         ("category", category))
        
        custom_metals = ["Платина", "Титан", "Розово злато", "Бяло злато"]
        for metal in custom_metals:
            cursor.execute("INSERT OR IGNORE INTO custom_values (type, value) VALUES (?, ?)", 
                         ("metal_type", metal))
        
        custom_stones = ["Танзанит", "Александрит", "Опал", "Турмалин", "Топаз", "Гранат"]
        for stone in custom_stones:
            cursor.execute("INSERT OR IGNORE INTO custom_values (type, value) VALUES (?, ?)", 
                         ("stone_type", stone))
        
        print("✅ Custom values created")
        
        # Commit all changes
        conn.commit()
        conn.close()
        
        print("🎉 Test data population completed successfully!")
        print()
        print("📊 SUMMARY:")
        print(f"   • Created {len(test_shops)} test shops")
        print(f"   • Added {len(test_items)} items to warehouse")
        print(f"   • Distributed items to shops (warehouse→shop transfers)")
        print(f"   • Generated sales for last 45 days (shop→customer)")
        print(f"   • Added custom categories, metals, and stones")
        print()
        print("🏗️ ARCHITECTURE CONFIRMED:")
        print("   • WAREHOUSE: items.stock_quantity (central inventory)")
        print("   • SHOPS: shop_items.quantity (distributed inventory)")
        print("   • SALES: shop_id tracked, only shop inventory affected")
        print()
        print("🚀 You can now test all export functionalities!")
        print("   Test the comprehensive report to see how data flows!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating test data: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_data():
    """Remove all test data from database"""
    try:
        db_path = os.path.join("data", "jewelry.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🧹 Cleaning up test data...")
        
        # Delete in reverse order to respect foreign keys
        cursor.execute("DELETE FROM sales")
        cursor.execute("DELETE FROM shop_items") 
        cursor.execute("DELETE FROM items")
        cursor.execute("DELETE FROM custom_values")
        
        # Keep only the first shop, delete test shops
        cursor.execute("DELETE FROM shops WHERE name != 'Магазин 1'")
        
        conn.commit()
        conn.close()
        
        print("✅ Test data cleanup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up test data: {e}")
        return False

def main():
    """Main function with user interface"""
    print("=" * 60)
    print("  JEWELRY MANAGEMENT - TEST DATA POPULATION")
    print("=" * 60)
    print()
    
    while True:
        print("🤔 What would you like to do?")
        print("1) Populate test data")
        print("2) Cleanup test data")
        print("3) Exit")
        print()
        
        choice = input("Enter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            print()
            if populate_test_data():
                print()
                print("✅ SUCCESS! Test data has been populated.")
                print("   You can now test export functionalities.")
            else:
                print()
                print("❌ FAILED! Could not populate test data.")
            break
            
        elif choice == "2":
            print()
            confirm = input("⚠️  Are you sure you want to delete all test data? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                if cleanup_test_data():
                    print()
                    print("✅ SUCCESS! Test data has been cleaned up.")
                else:
                    print()
                    print("❌ FAILED! Could not cleanup test data.")
            else:
                print("Cleanup cancelled.")
            break
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            print()
    
    print()
    input("📋 Press Enter to exit...")

if __name__ == "__main__":
    main()
