import customtkinter as ctk
import pandas as pd
import sqlite3
from src.utils.db_inventory_manager import DBInventoryManager

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

    def daily_sales(self):
        # Line graph of daily sales

        # Today's sales label
        pass

    def top_10_products(self):
        # show by Bar Graph
        pass

    

    def data_analysis(self):

        data = self.db_manager.get_inventory()

        query = ''
        inventory_df = pd.read_sql_query()
        
        pass