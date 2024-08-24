import re
from urllib.parse import urlparse


def is_valid_url(url):
    """Check if the URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_headers(headers):
    """Check if headers are in key|value format."""
    for header in headers.split("|"):
        if ":" not in header:
            return False
        key, value = header.split(":", 1)
        if not key.strip() or not value.strip():
            return False
    return True
