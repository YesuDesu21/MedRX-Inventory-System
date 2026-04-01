import sys
import os
# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from utils.db_inventory_manager import DBInventoryManager
from utils.db_transactions_manager import DBTransactionsManager

class DataAnalysis:
    def __init__(self):
        self.inventory_manager = DBInventoryManager()
        self.transactions_manager = DBTransactionsManager()
        
    def analyze(self):
        pass
