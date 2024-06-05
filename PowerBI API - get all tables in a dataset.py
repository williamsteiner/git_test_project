import requests

# Authentication
tenant_id = '36ae21d1-a6d1-497a-ba7c-e2bae38c151b'
client_id = '635741d9-9647-4a60-844e-8c3928f639b3'
client_secret = ''

# Obtain Access Token
authority = f'https://login.microsoftonline.com/{tenant_id}'
resource = 'https://analysis.windows.net/powerbi/api'
token_url = f'{authority}/oauth2/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource
}
token_response = requests.post(token_url, data=token_data)
token_response.raise_for_status()
access_token = token_response.json()['access_token']

# Get Dataset ID
dataset_id = '5f467043-3eec-45f3-bffd-08453ee64377'

# List Tables
tables_url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
tables_response = requests.get(tables_url, headers=headers)
tables_response.raise_for_status()

# Process Response
tables_data = tables_response.json()['value']
table_names = [table['name'] for table in tables_data]

# Print Table Names
print("Tables in the dataset:")
for table_name in table_names:
    print(table_name)
