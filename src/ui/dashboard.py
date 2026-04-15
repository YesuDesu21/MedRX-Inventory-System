import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from src.data_analysis.data_analysis import DataAnalysis
from src.utils.logger import log_user_action
"""
Dashboard ui class for the MedRX Inventory System
"""

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.analytics = DataAnalysis()
        self.create_dashboard()
        log_user_action("Opened Dashboard", "Dashboard")
    
    def create_dashboard(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self.parent)
        self.main_scrollable.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.main_scrollable)
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="MedRX Dashboard", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Statistics Row
        self.create_stats_row()
        
        # Charts Container
        charts_frame = ctk.CTkFrame(self.main_frame)
        charts_frame.pack(fill="both", expand=True, pady=10)
        
        # Left Column - Daily Sales Chart
        left_frame = ctk.CTkFrame(charts_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.daily_sales(left_frame)
        
        # Right Column - Top Products Chart
        right_frame = ctk.CTkFrame(charts_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.top_10_products(right_frame)
        
        # Priority Lists Container
        priority_frame = ctk.CTkFrame(self.main_frame)
        priority_frame.pack(fill="both", expand=True, pady=10)
        
        # Priority Lists Side by Side
        left_priority = ctk.CTkFrame(priority_frame)
        left_priority.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_priority = ctk.CTkFrame(priority_frame)
        right_priority.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.priority_expiration(left_priority)
        self.priority_products(right_priority)
    
    def create_stats_row(self):
        """Create statistics row with key metrics"""
        stats_frame = ctk.CTkFrame(self.main_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Get today's sales data
        sales_today = self.analytics.get_sales_today()
        total_sales_today = sales_today['total_price'].sum() if not sales_today.empty else 0
        
        # Get inventory counts
        inventory_df = self.analytics.inventory_df
        total_products = len(inventory_df) if not inventory_df.empty else 0
        low_stock_count = len(self.analytics.priority_products()) if not inventory_df.empty else 0
        expiring_count = len(self.analytics.priority_expiration()) if not inventory_df.empty else 0
        
        # Create stat cards
        stats_data = [
            ("Today's Sales", f"PHP {total_sales_today:,.2f}", "#4CAF50"),
            ("Total Products", str(total_products), "#2196F3"),
            ("Low Stock Items", str(low_stock_count), "#FF9800"),
            ("Expiring Soon", str(expiring_count), "#F44336")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = ctk.CTkFrame(stats_frame)
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12))
            title_label.pack(pady=(10, 5))
            
            value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=18, weight="bold"))
            value_label.pack(pady=(0, 10))

    def daily_sales(self, parent):
        """Create line graph of daily sales"""
        # Container frame
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(container, text="Daily Sales Trend", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(10, 5))
        
        # Get sales data
        sales_data = self.analytics.sales_graph_data()
        
        # Create matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if not sales_data.empty:
            # Sort by date
            sales_data = sales_data.sort_index()
            
            # Get last 30 days for better visualization
            end_date = sales_data.index.max()
            start_date = end_date - timedelta(days=30)
            recent_sales = sales_data[sales_data.index >= start_date]
            
            ax.plot(recent_sales.index, recent_sales.values, 
                   color='#2196F3', linewidth=2, marker='o', markersize=4)
            ax.fill_between(recent_sales.index, recent_sales.values, 
                           alpha=0.3, color='#2196F3')
            
            # Format x-axis
            ax.tick_params(axis='x', rotation=45)
            ax.set_xlabel('Date')
            ax.set_ylabel('Sales (PHP)')
            ax.set_title('Last 30 Days')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No sales data available', 
                   ha='center', va='center', transform=ax.transAxes)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def sales_today(self):
        # Today's sales label e.g sales today is P4000.00
        sales_today = self.analytics.get_sales_today()

    def top_10_products(self, parent):
        """Create bar chart of top 10 products"""
        # Container frame
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(container, text="Top 10 Products", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(10, 5))
        
        # Get top products data
        top_products = self.analytics.frequently_bought_products()
        
        # Create matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if not top_products.empty:
            # Create horizontal bar chart
            y_pos = np.arange(len(top_products))
            bars = ax.barh(y_pos, top_products.values, color='#4CAF50')
            
            # Customize bars with gradient effect
            for bar in bars:
                bar.set_alpha(0.8)
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(top_products.index, fontsize=9)
            ax.set_xlabel('Units Sold')
            ax.set_title('Most Frequently Purchased')
            ax.grid(True, alpha=0.3, axis='x')
            
            # Add value labels on bars
            for i, v in enumerate(top_products.values):
                ax.text(v + 0.1, i, str(v), va='center', fontsize=9)
        else:
            ax.text(0.5, 0.5, 'No product data available', 
                   ha='center', va='center', transform=ax.transAxes)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))


    def priority_expiration(self, parent):
        """Create visual list of products expiring soon"""
        # Container frame
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(container, text="Expiring Soon (6 Months)", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(10, 5))
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(container, height=200)
        scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Get expiring products
        expiring_products = self.analytics.priority_expiration()
        
        if not expiring_products.empty:
            # Sort by expiration date (earliest first)
            expiring_products = expiring_products.sort_values('expiration_date')
            
            for _, product in expiring_products.iterrows():
                # Calculate days until expiration
                days_until = (product['expiration_date'] - pd.Timestamp.now()).days
                urgency_color = "#F44336" if days_until < 30 else "#FF9800" if days_until < 90 else "#FFC107"
                
                # Product frame
                product_frame = ctk.CTkFrame(scrollable)
                product_frame.pack(fill="x", pady=2, padx=5)
                
                # Product info
                info_text = f"{product['item_name']} - {days_until} days"
                info_label = ctk.CTkLabel(product_frame, text=info_text, 
                                        font=ctk.CTkFont(size=11))
                info_label.pack(side="left", padx=10, pady=5)
                
                # Urgency indicator
                urgency_label = ctk.CTkLabel(product_frame, text="!", 
                                           text_color=urgency_color,
                                           font=ctk.CTkFont(size=12, weight="bold"))
                urgency_label.pack(side="right", padx=10, pady=5)
        else:
            no_data_label = ctk.CTkLabel(scrollable, text="No products expiring soon")
            no_data_label.pack(pady=20)

    def priority_products(self, parent):
        """Create visual list of products needing restock"""
        # Container frame
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(container, text="Low Stock Alert", 
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=(10, 5))
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(container, height=200)
        scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Get low stock products
        low_stock_products = self.analytics.priority_products()
        
        if not low_stock_products.empty:
            # Sort by quantity (lowest first)
            low_stock_products = low_stock_products.sort_values('quantity')
            
            for _, product in low_stock_products.iterrows():
                # Determine urgency based on quantity
                urgency_color = "#F44336" if product['quantity'] < 5 else "#FF9800"
                
                # Product frame
                product_frame = ctk.CTkFrame(scrollable)
                product_frame.pack(fill="x", pady=2, padx=5)
                
                # Product info
                info_text = f"{product['item_name']} - {int(product['quantity'])} units"
                info_label = ctk.CTkLabel(product_frame, text=info_text, 
                                        font=ctk.CTkFont(size=11))
                info_label.pack(side="left", padx=10, pady=5)
                
                # Urgency indicator
                urgency_label = ctk.CTkLabel(product_frame, text="!", 
                                           text_color=urgency_color,
                                           font=ctk.CTkFont(size=12, weight="bold"))
                urgency_label.pack(side="right", padx=10, pady=5)
        else:
            no_data_label = ctk.CTkLabel(scrollable, text="All products well stocked")
            no_data_label.pack(pady=20)
