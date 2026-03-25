import tkinter.ttk as ttk
from src.database_manager import DatabaseManager

class Transaction:
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.create_transaction()

    #if new transaction then subtract to quantity
    def create_transaction(self):
        pass

    #if delete transaction, add back to quantity
    def delete_transaction(self):
        pass