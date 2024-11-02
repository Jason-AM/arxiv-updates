import requests
from keys import GEMINI_KEY

# Define the endpoint and API key
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b-latest:generateContent"
api_key = GEMINI_KEY  

# Set headers and JSON payload
headers = {
    "Content-Type": "application/json",
}

def gemini_request(prompt:str):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Send the POST request
    response = requests.post(f"{url}?key={api_key}", headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        return data
    else:
        print("Request failed:", response.status_code, response.text)
