import requests

# The URL will be your local server
url = "http://localhost:8000/webhook"

# Sample payload matching the expected format
payload = {
    "sessionInfo": {
        "parameters": {
            "hsn_code": ["01011090"]  # Can be a single string or list of codes
        }
    }
}

# Send POST request
response = requests.post(url, json=payload)
print(response.json())