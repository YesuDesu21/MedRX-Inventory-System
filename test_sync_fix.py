#!/usr/bin/env python3
"""
Test script to verify Google Sheets sync functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.database_manager import DatabaseManager

def test_sync():
    print("Testing Google Sheets sync...")
    
    try:
        # Initialize database manager
        db = DatabaseManager()
        
        # Test sync_to_sheets
        print("\n1. Testing sync_to_sheets...")
        result = db.sync_manager.sync_to_sheets()
        if result:
            print("✓ sync_to_sheets successful")
        else:
            print("✗ sync_to_sheets failed")
        
        # Show current inventory data
        print("\n2. Current inventory data:")
        inventory = db.get_inventory()
        print(f"Found {len(inventory)} items in database")
        if inventory:
            print("Sample data (first 2 items):")
            for item in inventory[:2]:
                print(f"  ID: {item[0]}, Name: {item[1]}, Type: {item[2]}, Qty: {item[3]}")
        
        print("\n3. Test completed!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sync()
