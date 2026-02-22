import requests

url = "https://jsonplaceholder.typicode.com/comments/100"

updated_post = {
    "name": "Updated Post",
    "email": "[EMAIL_ADDRESS]",
    "body": "This is the updated content.",
    "postId": 100
}

response = requests.put(url, json=updated_post)

print("Status Code:", response.status_code)
print("Response Data:", response.json())