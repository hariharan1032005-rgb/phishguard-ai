import requests

def get_website_screenshot(url):
    api_key = "b815c8"

    screenshot_url = "https://api.screenshotmachine.com"

    params = {
        "key": api_key,
        "url": url,
        "dimension": "1024x768",
        "format": "png"
    }

    response = requests.get(screenshot_url, params=params)

    return response.url