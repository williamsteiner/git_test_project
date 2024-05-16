import pandas as pd
import requests
import datetime

current_year = datetime.datetime.now().year
previous_year = current_year -1 
 
# Note: to get the hashcode below run the postman script and click the </> code icon to get hashcode
payload = 'grant_type=client_credentials'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic c2ItZG1vZGF0YS1vd2ktUHJvZHVjdGlvbiF0MTEyNDM6YWFiZGU5NTMtMTQ5MS00YTlhLThhY2MtYWFjOTlkMDA5ZmJlJHNnTHJzU0FWWnRsQ2xKMks4ckRmUXRfS1Fsdmxqc3UzWWxacVZyVUJYNzg9'
}

# Token API URL
token_api_url = 'https://owi.authentication.us10.hana.ondemand.com/oauth/token'

# Initial URL for fetching the first 1000 rows 
get_data_url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/odata/v4/dmo/" 
data_table_name = "Pricerequest"
 

def get_access_token(token_api_url):
    try:
        # Make a GET request to the API endpoint 
        response = requests.request("POST", token_api_url, headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Convert the response to JSON format
            json_data = response.json()

            # Extract the value associated with the key "access_token"
            access_token = json_data.get('access_token')

            if access_token:
                return access_token
            else:
                print("No access token found in the JSON response.")
                return None
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            return None
        
    except Exception as e:
        print("An error occurred:", e)
        return None

def fetch_all_rows(url, access_token):
    all_rows = [] 
    payload = {}
    headers = {
      'Authorization': 'Bearer ' + access_token
    }
 
    while url: 
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break
        data = response.json() #example: rows = data.get('value', [])
        #data_d = data.get('d')
        #rows = data_d.get('results')
        rows = data.get('value')
        all_rows.extend(rows)
        #url = data_d.get('__next')
        url_next =  data.get('@odata.nextLink')
        if url_next is None:
            break  # Exit the loop if var is None
        url = get_data_url + url_next
    return all_rows
 

# Call the get_access_token function to retrieve the access token
access_token = get_access_token(token_api_url) 

# odata filter  
filter = "?$filter=year(CREATE_DATE) ge " + str(previous_year)
# Initial URL for fetching the first 1000 rows 
#url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/v2/odata/v4/dmo/Pricerequest" + filter 
url = get_data_url + data_table_name + filter

# Fetch all rows
all_rows = fetch_all_rows(url, access_token)

# Print the total number of rows fetched
print("Total number of rows fetched:", len(all_rows))
# Print the total number of rows fetched
print("Total number of rows fetched:", len(all_rows))

df = pd.DataFrame(all_rows)   
print (df)    


# Save DataFrame as a CSV/xlsx file
#df.to_csv('semantic_model.csv', index=False)
df.to_excel('price_request_semantic_model.xlsx', index=False)