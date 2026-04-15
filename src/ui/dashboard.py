import customtkinter as ctk
import pandas as pd
import sqlite3
from src.utils.db_inventory_manager import DBInventoryManager

"""
Dashboard ui class for the MedRX Inventory System
"""

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DBInventoryManager()
        self.create_dashboard()
    
    def create_dashboard(self):
        label = ctk.CTkLabel(self.parent, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)
        
        stats_label = ctk.CTkLabel(self.parent, text="Statistics here")
        stats_label.pack(pady=10)

        # line graph - sales per day
        self.daily_sales()

        # sales today
        self.sales_today()


        # top 10 bought products
        self.top_10_products()


        # visual  list of product expiration date within 6 months
        self.priority_expiration()


        # visual list of products needed to restock
        self.priority_products()



    def daily_sales(self):
        # Line graph of daily sales

        # Today's sales label
        pass

    def sales_today(self):
        # Today's sales label
        pass

    def top_10_products(self):
        # show by Bar Graph
        pass

    def priority_expiration(self):
        # visual list of product expiration date within 6 months
        pass

    def priority_products(self):
        # visual list of products needed to restock
        pass
