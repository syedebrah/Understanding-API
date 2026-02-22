import requests

url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.delete(url)

print("Status Code:", response.status_code)
print("Response:", response.text) 