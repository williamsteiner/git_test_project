import requests
import pandas as pd

# Define your Power BI credentials - use value for secret
tenant_id = '36ae21d1-a6d1-497a-ba7c-e2bae38c151b'
client_id = '1d8a8190-8c2b-4d87-9c9b-8bc970e4c46c'
client_secret = ''   
resource_url = 'https://analysis.windows.net/powerbi/api'
 

# Get access token
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource_url
}
response = requests.post(token_url, data=payload)
access_token = response.json()['access_token']

# Define the dataset ID
#dataset_id = '5f467043-3eec-45f3-bffd-08453ee64377/details?ctid=36ae21d1-a6d1-497a-ba7c-e2bae38c151b'
dataset_id = '5f467043-3eec-45f3-bffd-08453ee64377'

# Define the export URL
export_url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/Default.GetRows'

# Define export parameters
export_params = {
    '$top': 1000,  # Adjust based on your dataset size
    '$format': 'csv'
}

# Make the export request
export_response = requests.get(export_url, headers={'Authorization': f'Bearer {access_token}'}, params=export_params)
reason = export_response.reason
status_code = export_response.status_code
print("status code:" + str(status_code) + ", reason: " + reason)

# Write the CSV data to a file
with open('MyDataSet.csv', 'wb') as f:
    f.write(export_response.content)

print('Dataset exported successfully to MyDataSet.csv')