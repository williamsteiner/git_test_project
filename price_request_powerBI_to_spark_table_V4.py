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
# Get Odata URL
get_data_url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/odata/v4/dmo/" 
data_table_name = "Pricerequest"
filter = "?$filter=year(CREATE_DATE) ge " + str(previous_year)
 

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
        data = response.json()  
        rows = data.get('value')
        all_rows.extend(rows) 
        url_next =  data.get('@odata.nextLink')
        if url_next is None:
            break  # Exit the loop if var is None
        url = get_data_url + url_next
    return all_rows
 

# Call the get_access_token function to retrieve the access token
access_token = get_access_token(token_api_url) 
url = get_data_url + data_table_name + filter
# Fetch all rows
all_rows = fetch_all_rows(url, access_token)

# Print the total number of rows fetched
print("Total number of rows fetched:", len(all_rows))

df = pd.DataFrame(all_rows)   
# print (df)    


# ---------------------------------------------------------- #
print("start spark table write process")
from pyspark.sql import SparkSession        # pip install pyspark
from pyspark.sql.types import StructType, StructField, StringType, LongType

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("CreateDataFrame") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .enableHiveSupport() \
    .getOrCreate() 

# Convert pandas DataFrame rows to list of tuples
data = [tuple(row) for row in df.to_numpy()]

# Get the schema from the first row of data
first_row = df.iloc[0]
schema = StructType([
    StructField(col, 
                LongType() if isinstance(first_row[i], int) else StringType(), 
                True) 
    for i, col in enumerate(df.columns)
])

# Create PySpark DataFrame
df_spark = spark.createDataFrame(data, schema)

# Save PySpark DataFrame as a table with the desired name below
df_spark.write.mode("overwrite").saveAsTable("BillTest_PR_V4")

print("spark table write process COMPLETED")

# Stop SparkSession
spark.stop()