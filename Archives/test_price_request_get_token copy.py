import requests

url = "https://owi.authentication.us10.hana.ondemand.com/oauth/token"

'''payload = 'grant_type=password&username=akothari%40owi.com&password=Arpit%40123'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic c2ItZG1vZGF0YS1vd2ktUHJvZHVjdGlvbiF0MTEyNDM6YWFiZGU5NTMtMTQ5MS00YTlhLThhY2MtYWFjOTlkMDA5ZmJlJHNnTHJzU0FWWnRsQ2xKMks4ckRmUXRfS1Fsdmxqc3UzWWxacVZyVUJYNzg9',
  'Cookie': 'X-Uaa-Csrf=YtAEU3PcNyDxDQZysAN4GZ'
}'''

# Note: to get the hashcode below run the postman script and click the </> code icon to get hashcode
payload = 'grant_type=client_credentials'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic c2ItZG1vZGF0YS1vd2ktUHJvZHVjdGlvbiF0MTEyNDM6YWFiZGU5NTMtMTQ5MS00YTlhLThhY2MtYWFjOTlkMDA5ZmJlJHNnTHJzU0FWWnRsQ2xKMks4ckRmUXRfS1Fsdmxqc3UzWWxacVZyVUJYNzg9'
}

access_token = False
response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)
#print("token: " + response["access_token"])

'''
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert the response to JSON format
    json_data = response.json()

    # Extract the value associated with the key "access_token"
    access_token = json_data.get('access_token')

    if access_token:
        print("Access token:", access_token)
    else:
        print("No access token found in the JSON response.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
'''

def get_access_token(api_url):
    try:
        # Make a GET request to the API endpoint
        #response = requests.get(api_url)
        response = requests.request("POST", url, headers=headers, data=payload)

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

# Example usage: 
access_token = get_access_token(url)
if access_token:
    print("Access token:", access_token)  