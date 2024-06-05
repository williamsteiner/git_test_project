import requests
import json
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

tenant_id = '36ae21d1-a6d1-497a-ba7c-e2bae38c151b'
client_id = '635741d9-9647-4a60-844e-8c3928f639b3'
client_secret = ''
authority = f'https://login.microsoftonline.com/{tenant_id}'
resource = 'https://analysis.windows.net/powerbi/api'

# Step 1: Get Access Token
body = {
    'resource': resource,
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

url = f'{authority}/oauth2/token'
response = requests.post(url, data=body)
response.raise_for_status()

token = response.json().get('access_token')

# Step 2: Export Power BI Data
dataset_id = 'your_dataset_id'
export_url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(export_url, headers=headers)
response.raise_for_status()

data = response.json()
tables = data['value']

# Step 3: Save Data to Excel
with pd.ExcelWriter('ExportedData.xlsx', engine='openpyxl') as writer:
    for table in tables:
        table_name = table['name']
        table_url = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/tables/{table_name}/rows'
        response = requests.get(table_url, headers=headers)
        response.raise_for_status()
        rows = response.json()['value']
        df = pd.DataFrame(rows)
        df.to_excel(writer, sheet_name=table_name, index=False)

# Step 4: Upload to SharePoint
sharepoint_url = 'https://oldworld.sharepoint.com/sites/MarketingPOS'
sharepoint_site_name = 'Marketing POS'
sharepoint_folder_name = 'PowerBI Files/Retail POS and INV/POS-ALL BI Data Model Extract File'  # https://oldworld.sharepoint.com/:f:/s/MarketingPOS/EqOcZirSENFKtfBTng3_qMMBar1yIkutiT9H2WB0YmpSKw?e=dZjSeY

ctx = ClientContext(sharepoint_url).with_credentials(ClientCredential(client_id, client_secret))
target_folder = ctx.web.get_folder_by_server_relative_url(f'{sharepoint_site_name}/{sharepoint_folder_name}')
with open('ExportedData.xlsx', 'rb') as content_file:
    file_content = content_file.read()
    target_folder.upload_file('ExportedData.xlsx', file_content).execute_query()

print('File uploaded to SharePoint successfully')
