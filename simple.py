import requests   # library to work with APIs

# Step 1: API URL
url = "https://api.agify.io/?name=syed"

# Step 2: Send GET request to API
response = requests.get(url)

# Step 3: Convert response into JSON (dictionary format)
data = response.json()

# Step 4: Print the full response
print("Full API Response:", data)

# Step 5: Access specific values
print("Name:", data["name"])
print("Predicted Age:", data["age"])
print("Count:", data["count"])