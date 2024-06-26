import requests

workspace_id = '7517477f-7b04-4c6d-86d9-7897b2558b73'
report_id = '19952fec-5df9-45b9-8537-c1312159ed22'
access_level = 'View'  # View or Edit
token_duration_minutes = 60  # Token duration in minutes

access_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6IkZTX0tfeUh4UG9BS2NEWThZVk5nV2ZJS0RQWlg3cnFnYWlLalFqeXlmakkiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zNmFlMjFkMS1hNmQxLTQ5N2EtYmE3Yy1lMmJhZTM4YzE1MWIvIiwiaWF0IjoxNzE2Mzk5ODgzLCJuYmYiOjE3MTYzOTk4ODMsImV4cCI6MTcxNjQwMzc4MywiYWlvIjoiRTJOZ1lMaWZrWERLa1pHMzQrdys1MXdPaWYydkFBPT0iLCJhcHBfZGlzcGxheW5hbWUiOiJNYXJrZXRpbmcgV2Vla2x5IFBPUyIsImFwcGlkIjoiNjM1NzQxZDktOTY0Ny00YTYwLTg0NGUtOGMzOTI4ZjYzOWIzIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMzZhZTIxZDEtYTZkMS00OTdhLWJhN2MtZTJiYWUzOGMxNTFiLyIsImlkdHlwIjoiYXBwIiwib2lkIjoiZTE4YTg5NzEtNjE1Mi00YTkwLWI5YjYtNDVlNGZiYzdkNGIwIiwicmgiOiIwLkFSY0EwU0d1TnRHbWVrbTZmT0s2NDR3Vkd3TUFBQUFBQUFBQXdBQUFBQUFBQUFBWEFBQS4iLCJzdWIiOiJlMThhODk3MS02MTUyLTRhOTAtYjliNi00NWU0ZmJjN2Q0YjAiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiTkEiLCJ0aWQiOiIzNmFlMjFkMS1hNmQxLTQ5N2EtYmE3Yy1lMmJhZTM4YzE1MWIiLCJ1dGkiOiJWUkNieUE2UExrbV9ic25vTXY0VUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyIwOTk3YTFkMC0wZDFkLTRhY2ItYjQwOC1kNWNhNzMxMjFlOTAiXSwieG1zX3RjZHQiOjE0NTgyNTE2NDh9.bHVS1Su4i2NcTWoaL8EcLfaM22GbFcUb7VvVnw5go-cz-L4IbfeeGyOiDSY76K9gRFaiUcuM-c0KmqeLh5xI8NfEFsKy7tIKroca-HjbgYhStQgaDr2peziLQob14Yw-e7Pt3HMCSSvoNDtkPT_96TjOJrqcpYOoZKXgLc_F85nO1KwoUdvbE-yWH_5ZliWpSNLvtkzdf33LhRskdPd3lqenpMyWVM1Fbngs2lwdo0tl_KK9zxnMWdjUevFC2wHQQs6JAGHXhm-wJY-_890A09sD9RJUvgSGBdBEZPlJdNw3eRz9pftACvR3r5MLMNAC3ti45wc5cdMKutNTwbeACQ'

generate_token_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/GenerateToken'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token  # Include your Azure AD access token here
}
data = {
    'accessLevel': access_level,
    'tokenType': 'Embed',
    'expiration': f'{token_duration_minutes}M'  # Token expiration time
}

response = requests.post(generate_token_url, json=data, headers=headers)
response.raise_for_status()

embed_token = response.json()['token']
print('Embed Token:', embed_token)
