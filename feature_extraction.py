<<<<<<< HEAD
import re

def extract_features(url):

    url_length = len(url)

    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    https = 1 if url.startswith("https") else 0

    dots = url.count('.')

    hyphen = url.count('-')

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
=======
import re

def extract_features(url):

    url_length = len(url)

    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    https = 1 if url.startswith("https") else 0

    dots = url.count('.')

    hyphen = url.count('-')

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
>>>>>>> 3292d845d44f5701216bdfb571c1a9aa61eb0d04
    ]