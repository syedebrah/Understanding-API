import requests

url = "https://jsonplaceholder.typicode.com/posts"

new_post = {
    "title": "My New Post",
    "body": "This is the content of my new post.",
    "userId": 1000
}

response = requests.post(url, json=new_post)

print("Status Code:", response.status_code)
print("Response Data:", response.json())
