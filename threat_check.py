<<<<<<< HEAD
import requests
import json

API_KEY = "AIzaSyAvI4i7wJH83kSovnjBlMe6LSqKEk3IlV4"

def check_url(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    data = {
        "client": {
            "clientId": "phishguard-ai",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    response = requests.post(endpoint, json=data)
    result = response.json()

    print("API Response:", result)   # Debug output

    if result.get("matches"):
        print("⚠️ WARNING: Dangerous URL detected!")
    else:
        print("✅ This URL appears safe.")

if __name__ == "__main__":
    url = input("Enter URL to check: ")
=======
import requests
import json

API_KEY = "AIzaSyAvI4i7wJH83kSovnjBlMe6LSqKEk3IlV4"

def check_url(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    data = {
        "client": {
            "clientId": "phishguard-ai",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    response = requests.post(endpoint, json=data)
    result = response.json()

    print("API Response:", result)   # Debug output

    if result.get("matches"):
        print("⚠️ WARNING: Dangerous URL detected!")
    else:
        print("✅ This URL appears safe.")

if __name__ == "__main__":
    url = input("Enter URL to check: ")
>>>>>>> 3292d845d44f5701216bdfb571c1a9aa61eb0d04
    check_url(url)