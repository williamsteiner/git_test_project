import pandas as pd
import requests
import datetime

current_year = datetime.datetime.now().year
previous_year = current_year -1

payload = 'grant_type=password&username=akothari%40owi.com&password=Arpit%40123'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic c2ItZG1vZGF0YS1vd2ktUHJvZHVjdGlvbiF0MTEyNDM6YWFiZGU5NTMtMTQ5MS00YTlhLThhY2MtYWFjOTlkMDA5ZmJlJHNnTHJzU0FWWnRsQ2xKMks4ckRmUXRfS1Fsdmxqc3UzWWxacVZyVUJYNzg9',
  'Cookie': 'X-Uaa-Csrf=YtAEU3PcNyDxDQZysAN4GZ'
}

 
#def main():


def get_access_token(api_url):
    try:
        # Make a GET request to the API endpoint
        #response = requests.get(api_url)
        response = requests.request("POST", api_url, headers=headers, data=payload)

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


def get_data(url, access_token):
    try:
      payload = {}
      headers = {
        'Authorization': 'Bearer ' + access_token
      }

      response = requests.request("GET", url, headers=headers, data=payload)
              # Check if the request was successful (status code 200)
      if response.status_code == 200:
          # Convert the response to JSON format
          json_data = response.json()

          # Extract the value associated with the key  
          data_d = json_data.get('d')
          data_results = data_d.get('results')

          if data_results:
              return data_results
          else:
              print("No data found in the JSON response.")
              return None
      else:
          print("Failed to retrieve data. Status code:", response.status_code)
          return None
    #print(response.text)


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
        #data = get_data(url, access_token)
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break
        data = response.json()
        #rows = data.get('value', [])
        data_d = data.get('d')
        rows = data_d.get('results')
        all_rows.extend(rows)
        url = data_d.get('__next')
    return all_rows




#if __name__ == "__main__":
#    main()

# Example API URL
api_url = 'https://owi.authentication.us10.hana.ondemand.com/oauth/token'

# Call the get_access_token function to retrieve the access token
access_token = get_access_token(api_url) 

# get data
filter = "?$top=50000&$skip=0&$inlinecount=allpages&$filter=year(CREATE_DATE) ge " + str(previous_year)

# Initial URL for fetching the first 1000 rows
#initial_url = "https://example.com/v2/odata/v4/dmo/Pricerequest?$top=1000"

url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/v2/odata/v4/dmo/Pricerequest" + filter
#data_results = get_data(url, access_token)

# Fetch all rows
all_rows = fetch_all_rows(url, access_token)

# Print the total number of rows fetched
print("Total number of rows fetched:", len(all_rows))


df = pd.DataFrame(all_rows)  # ,columns=['Name','Age']
print (df)    
