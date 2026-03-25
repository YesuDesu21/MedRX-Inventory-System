import json

# Read credentials and get service account email
with open('credentials.json', 'r') as f:
    creds = json.load(f)

service_email = creds.get('client_email')
print(f"Service Account Email: {service_email}")
print("\nCopy this email and share your Google Sheet with it as 'Editor'")
