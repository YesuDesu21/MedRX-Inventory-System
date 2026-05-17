# Logic for cloud operations

import cloud_connector

# Needs to get or send data to supabase

class CloudManager:
    def __init__(self):
        self.cloud = cloud_connector.CloudConnector()
        pass

    def get_data_from_cloud(self):
        pass
    def send_data_to_cloud(self):
        pass


