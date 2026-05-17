import os 
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class CloudConnector:
    '''
    Deals with supabase cloud database
    '''
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        
        print(f"Debug - URL: {self.url}")
        print(f"Debug - Key: {'***' if self.key else 'None'}")
        
        self.supabase = create_client(self.url, self.key)

# if __name__ == "__main__":
#     cloud = CloudConnector()
#     print(f"URL: {cloud.url}")
#     print(f"Key: {cloud.key}")
