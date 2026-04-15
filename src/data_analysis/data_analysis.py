import sys
import os
import pandas as pd
# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from utils.db_inventory_manager import DBInventoryManager
from utils.db_transactions_manager import DBTransactionsManager

class DataAnalysis:
    def __init__(self):
        self.inventory_manager = DBInventoryManager()
        self.transactions_manager = DBTransactionsManager()

        # Load data into DataFrames
        self.inventory_df = self.get_inventory_info()
        self.transactions_df = self.get_transaction_info()


    # Plots data point for line graph
    def sales_graph_data(self):
        transactions = self.transactions_df
        
        transactions_grouped = transactions.groupby('date_processed')['total_price'].sum()
        return transactions_grouped
    
    #Total Sales: P5000 (only sales by today)
    def get_sales_today(self):
        """Total sales for today"""
        sales_today = self.transactions_df[self.transactions_df['date_processed'].dt.date == pd.Timestamp.now().date()]
        return sales_today

    # example bar graph of top 10 bought products
    def frequently_bought_products(self):
        """Sales by N Products bought today"""
        frequently_bought = self.transactions_df['item_name'].value_counts().head(10)
        return frequently_bought

    def priority_expiration(self):
        """Products that are expiring soon (within 6 months)"""
        priority_expiration = self.inventory_df[self.inventory_df['expiration_date'] < pd.Timestamp.now() + pd.Timedelta(days=180)]
        return priority_expiration

    #if inventory/quantity less than 10
    def priority_products(self):
        """Products that need to be reordered"""
        priority_products = self.inventory_df[self.inventory_df['quantity'] < 10]
        return priority_products

    
    def get_inventory_info(self):
        """
        Read and return all inventory data from the products table as DataFrame
        Returns: pandas DataFrame with inventory information
        """
        try:
            data = self.inventory_manager.get_inventory()
            columns = [
                'product_id', 'item_name', 'product_type', 'quantity', 
                'unit_cost', 'price', 'medicine_type', 'expiration_date',
                'date_added', 'updated_date', 'item_name_duplicate', 'item_id'
            ]
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            print(f"Error getting inventory info: {e}")
            return pd.DataFrame()
    
    def get_transaction_info(self, search_term=None, date_from=None, date_to=None):
        """
        Read and return transaction data from the transactions table as DataFrame
        Parameters:
            search_term: Optional search term for transaction ID or item name
            date_from: Optional start date filter
            date_to: Optional end date filter
        Returns: pandas DataFrame with transaction information
        """
        try:
            data = self.transactions_manager.get_processed_transactions()
            columns = [
                'transaction_id','total_price','date_processed','user_id'
            ]
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            print(f"Error getting transaction data: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    data_analysis = DataAnalysis()
    # print(data_analysis.get_sales_today())
    # print(data_analysis.products_bought_today())
    # print(data_analysis.priority_expiration())
    # print(data_analysis.priority_products())
    # print(data_analysis.get_inventory_info())
    # print(data_analysis.get_transaction_info())
    print(data_analysis.sales_graph_data())
    