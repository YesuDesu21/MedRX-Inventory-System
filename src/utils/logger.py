import logging
import os
from datetime import datetime
from typing import Optional

class UserInteractionLogger:
    """Centralized logging system for user interactions in MedRX Inventory System"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.setup_loggers()
    
    def ensure_log_directory(self):
        """Create logs directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def setup_loggers(self):
        """Setup different loggers for different types of interactions"""
        # Main user interaction logger
        self.user_logger = self._create_logger(
            'user_interactions',
            os.path.join(self.log_dir, 'user_interactions.log'),
            level=logging.INFO
        )
        
        # System operations logger
        self.system_logger = self._create_logger(
            'system_operations',
            os.path.join(self.log_dir, 'system_operations.log'),
            level=logging.INFO
        )
        
        # Database operations logger
        self.db_logger = self._create_logger(
            'database_operations',
            os.path.join(self.log_dir, 'database_operations.log'),
            level=logging.INFO
        )
        
        # Error logger
        self.error_logger = self._create_logger(
            'errors',
            os.path.join(self.log_dir, 'errors.log'),
            level=logging.ERROR
        )
    
    def _create_logger(self, name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
        """Create and configure a logger"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        if logger.handlers:
            logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_user_action(self, action: str, module: str, details: Optional[str] = None, user: str = "Felino E. Doria"):
        """Log user interactions"""
        message = f"[{module}] {action}"
        if details:
            message += f" - {details}"
        message += f" (User: {user})"
        self.user_logger.info(message)
    
    def log_system_event(self, event: str, details: Optional[str] = None):
        """Log system events"""
        message = f"SYSTEM: {event}"
        if details:
            message += f" - {details}"
        self.system_logger.info(message)
    
    def log_database_operation(self, operation: str, table: str, details: Optional[str] = None):
        """Log database operations"""
        message = f"[{table}] {operation}"
        if details:
            message += f" - {details}"
        self.db_logger.info(message)
    
    def log_error(self, error: str, module: str, details: Optional[str] = None):
        """Log errors"""
        message = f"[{module}] ERROR: {error}"
        if details:
            message += f" - {details}"
        self.error_logger.error(message)
    
    def get_recent_logs(self, log_type: str = "user_interactions", lines: int = 100) -> list:
        """Get recent log entries"""
        log_file = os.path.join(self.log_dir, f"{log_type}.log")
        if not os.path.exists(log_file):
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.log_error(f"Failed to read log file: {e}", "Logger")
            return []

# Global logger instance
logger_instance = UserInteractionLogger()

# Convenience functions for easy access
def log_user_action(action: str, module: str, details: Optional[str] = None):
    """Log user interaction"""
    logger_instance.log_user_action(action, module, details)

def log_system_event(event: str, details: Optional[str] = None):
    """Log system event"""
    logger_instance.log_system_event(event, details)

def log_database_operation(operation: str, table: str, details: Optional[str] = None):
    """Log database operation"""
    logger_instance.log_database_operation(operation, table, details)

def log_error(error: str, module: str, details: Optional[str] = None):
    """Log error"""
    logger_instance.log_error(error, module, details)

def get_recent_logs(log_type: str = "user_interactions", lines: int = 100) -> list:
    """Get recent log entries"""
    return logger_instance.get_recent_logs(log_type, lines)
