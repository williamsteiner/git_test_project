import requests  # pip install requests

#url = "https://owi-production-dmodata-srv.cfapps.us10.hana.ondemand.com/v2/odata/v4/dmo/Pricerequest"
#payload = {}
#headers = {
#  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vb3dpLmF1dGhlbnRpY2F0aW9uLnVzMTAuaGFuYS5vbmRlbWFuZC5jb20vdG9rZW5fa2V5cyIsImtpZCI6ImtleS1pZC0xIiwidHlwIjoiSldUIiwiamlkIjogIjlYQzN4ZzdYVllncEVpVnpHMlNRTWxZUUI2SGI1ZCsvVmNpTzZYenFsV2s9In0.eyJqdGkiOiJkZDhlMTAxZDAwM2Q0ODMwOGUwYzFmOGQ4YzgyNzg3MiIsImV4dF9hdHRyIjp7ImVuaGFuY2VyIjoiWFNVQUEiLCJzdWJhY2NvdW50aWQiOiIzMWZkZWFmNC1jYTMxLTRlMGEtYTJiOC00YWQxYmQxYWMxZDEiLCJ6ZG4iOiJvd2kifSwidXNlcl91dWlkIjoiNDYwYjUwY2MtNWJhYi00NDYxLTkyNmQtZjQwY2U3ZDQ0YWM5IiwieHMudXNlci5hdHRyaWJ1dGVzIjp7fSwieHMuc3lzdGVtLmF0dHJpYnV0ZXMiOnsieHMucm9sZWNvbGxlY3Rpb25zIjpbIlNBUCBIQU5BIENsb3VkIFZpZXdlciIsIlN1YmFjY291bnQgU2VydmljZSBBZG1pbmlzdHJhdG9yIiwiV2VibWluX1VzZXJzIiwiRE1PX0FkbWluIiwiRGVzdGluYXRpb24gQWRtaW5pc3RyYXRvciIsIlBvcnRhbF9BZG1pbiIsIkNsb3VkIENvbm5lY3RvciBBZG1pbmlzdHJhdG9yIiwiU3ViYWNjb3VudCBBZG1pbmlzdHJhdG9yIiwiRE1PX1ByaWNlX1JlcXVlc3QiLCJXZWJtaW5fQWRtaW4iLCJPVyBBZG1pbiJdfSwiZ2l2ZW5fbmFtZSI6IkFycGl0IiwiZmFtaWx5X25hbWUiOiJrb3RoYXJpIiwic3ViIjoiODE3ZjYxNzYtNTRmNi00MGI0LWFlNDgtYTA1YjRlNTg4MjZlIiwic2NvcGUiOlsib3BlbmlkIl0sImNsaWVudF9pZCI6InNiLWRtb2RhdGEtb3dpLVByb2R1Y3Rpb24hdDExMjQzIiwiY2lkIjoic2ItZG1vZGF0YS1vd2ktUHJvZHVjdGlvbiF0MTEyNDMiLCJhenAiOiJzYi1kbW9kYXRhLW93aS1Qcm9kdWN0aW9uIXQxMTI0MyIsImdyYW50X3R5cGUiOiJwYXNzd29yZCIsInVzZXJfaWQiOiI4MTdmNjE3Ni01NGY2LTQwYjQtYWU0OC1hMDViNGU1ODgyNmUiLCJvcmlnaW4iOiJsZGFwIiwidXNlcl9uYW1lIjoiYWtvdGhhcmlAb3dpLmNvbSIsImVtYWlsIjoiYWtvdGhhcmlAb3dpLmNvbSIsImF1dGhfdGltZSI6MTcxNTI4NDkwNiwicmV2X3NpZyI6IjRmOGE2ZDEwIiwiaWF0IjoxNzE1Mjg0OTA2LCJleHAiOjE3MTUzMjgxMDYsImlzcyI6Imh0dHA6Ly9vd2kubG9jYWxob3N0OjgwODAvdWFhL29hdXRoL3Rva2VuIiwiemlkIjoiMzFmZGVhZjQtY2EzMS00ZTBhLWEyYjgtNGFkMWJkMWFjMWQxIiwiYXVkIjpbIm9wZW5pZCIsInNiLWRtb2RhdGEtb3dpLVByb2R1Y3Rpb24hdDExMjQzIl19.hCYE2P3UdQqVSFYsKsiBngwC-yP9yL-3Mo-U0xa4hjZk0dTEIY1bbOcgDnRWJfwjrNduwrJZytqI9yMJO89n2J83CNevmiasj4Nj1ilv-FXbFFOHhjvbJEh-yJDNHpIRWogROkFf_I1fReJ-2lrGqBq6OwnFtxpOFwdYHnVUxccl3n2xNgwlvdGskzTgQszIHZMNT20F_8Zn0EECv2v86oWbVRfy7_n04XODsxuNORHX7oMnhwKDlbmlTZuEfUdJYECA0S1uIGXFmmv8A2XmR9YhzjProWou8ghsSyTpOAIn1EqdF9_APXKH-VKy7nTlW5CguxB9_x-9TTayAxyWtJKk8ZV5W-iOr3vY4RevhJyxsJCsx7m7hnQg8z0zhnmUhQKehbbuzFlqU6MTKPXMNLEH1OeoR7p76ZBNeBRSY0dnRvEoFY-LKt77RaMYLGQ7EJ5rcsW2ln3iYYc9ZeyBnT7cJBq1puA3cmt1uXQB3isAXUJXOT0epUz3eDs0lfOL5aJBsGBQ4aJGhE7NwOKg1Dk6Tsq_HI3myJFiRbx8TrWVyEUadUzOI9N35EKsNqqiz_-fAVLsyPivgXi6xd-UNaof8zwl4XJWOpk-MivxOtQw9ATSbI7YbbPfH9fz1TbNUvT1tAIW1mFuAVvYk2W1Hsb3xtPjefWKpOfyc5d-gZc'
#}
#response = requests.request("GET", url, headers=headers, data=payload)
#print(response.text)

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