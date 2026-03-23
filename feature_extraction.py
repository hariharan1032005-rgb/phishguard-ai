import re

def extract_features(url):
    # 1. URL Length
    url_length = len(url)

    # 2. Check for IP Address in URL
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    # 3. Check for HTTPS
    https = 1 if url.startswith("https") else 0

    # 4. Count Dots
    dots = url.count('.')

    # 5. Count Hyphens
    hyphen = url.count('-')

    # 6. Search for Suspicious Keywords
    suspicious_words = 1 if re.search(
        r'login|verify|update|secure|account|bank|paypal|signin',
        url.lower()
    ) else 0

    return [
        url_length,
        has_ip,
        https,
        dots,
        hyphen,
        suspicious_words
    ]
