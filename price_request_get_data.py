import requests  # pip install requests

 
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