from price_request_get_token import get_access_token  # function name vs from price_request_get_token import *
from price_request_get_data import *

def main():
    # Example API URL
    api_url = 'https://owi.authentication.us10.hana.ondemand.com/oauth/token'

    # Call the get_access_token function to retrieve the access token
    access_token = get_access_token(api_url)
    '''    if access_token:
        print("***Access token:", access_token)
    else:
        print("Failed to retrieve access token.")'''
    
    # get data
    url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/v2/odata/v4/dmo/Pricerequest"
    data_results = get_data(url, access_token)

    if data_results:
        print("***data_results:", data_results)
    else:
        print("Failed to retrieve data_results.")

if __name__ == "__main__":
    main()
