import logging
from typing import Any
from urllib.parse import urlparse

from .const import CONF_HEADERS, CONF_URL

_LOGGER = logging.getLogger(__name__)

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


def validate_user_input(user_input: dict[str, Any]) -> dict[str, str]:
    """Validate the user input dictionary for URL and Headers.

    Args:
        user_input (dict[str, Any]): The user input containing URL and headers.

    Returns:
        dict[str, str]: A dictionary of errors with field names as keys and error messages as values.

    """
    errors = {}

    if not is_valid_url(user_input.get(CONF_URL, "")):
        errors[CONF_URL] = "invalid_url"
        _LOGGER.error("Invalid URL: %s", user_input.get(CONF_URL, ""))

    if user_input.get(CONF_HEADERS) and not is_valid_headers(user_input[CONF_HEADERS]):
        errors[CONF_HEADERS] = "invalid_headers"
        _LOGGER.error("Invalid Headers: %s", user_input[CONF_HEADERS])

    return errors
