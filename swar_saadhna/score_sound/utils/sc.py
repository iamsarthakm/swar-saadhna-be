import requests

url = "https://cpaas.messagecentral.com/auth/v1/authentication/token?country=IN&customerId=C-DE251B4119374E5&key=JTt9ckUuN144TyU4wqM=&scope=NEW"
payload = {}
headers = {"accept": "*/*"}
response = requests.request("GET", url, headers=headers, data=payload)
token = response.json()["token"]


url = "https://cpaas.messagecentral.com/verification/v2/verification/send?countryCode=91&customerId=C-DE251B4119374E5&flowType=SMS&mobileNumber=7455855660"

payload = {}
headers = {"authToken": token}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
