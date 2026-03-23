import re

def extract_features(url):
    url = url.lower()
    
    # 1. URL Length
    url_length = len(url)
    # 2. IP check
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    # 3. HTTPS check
    https = 1 if url.startswith("https") else 0
    # 4. Dots
    dots = url.count('.')
    # 5. Hyphens
    hyphen = url.count('-')
    # 6. Keywords
    suspicious = 1 if re.search(r'login|verify|update|secure|account|bank|paypal', url) else 0

    return [url_length, has_ip, https, dots, hyphen, suspicious]
