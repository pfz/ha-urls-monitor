"""The URL Monitor integration."""

import asyncio
import contextlib
from datetime import timedelta
import hashlib
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_HEADERS,
    CONF_INTERVAL,
    CONF_TIMEOUT,
    CONF_URL,
    DOMAIN,
    HASH_SIZE,
    LIMIT,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, entry) -> bool:
    """Set up the URLs monitor component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up URLs monitor from a config entry."""
    coordinator = UrlsMonitorCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    with contextlib.suppress(ValueError):
        await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    hass.data[DOMAIN].pop(entry.entry_id)

    return True


class UrlsMonitorCoordinator(DataUpdateCoordinator):
    """Class to manage fetching URLs data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize."""
        self.config = entry.data
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=entry.data[CONF_INTERVAL]),
        )

    def _parse_headers(self):
        """Parse the headers configuration."""
        raw_headers = self.config.get(CONF_HEADERS, "")
        if not raw_headers.strip():
            return {}

        headers = {}
        for header in raw_headers.split("|"):
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    async def _async_update_data(self):
        """Fetch data from URL."""
        url = self.config[CONF_URL]
        timeout = self.config[CONF_TIMEOUT]
        headers = self._parse_headers()

        try:
            async with aiohttp.ClientSession() as session:
                async with asyncio.timeout(timeout):
                    async with session.get(url, headers=headers) as response:
                        response.raise_for_status()
                        text = await response.text()
                        content_length = response.headers.get(
                            "content-length", "unknown"
                        )

            data_hash = hashlib.md5(text.encode("utf-8")).hexdigest()[:HASH_SIZE]
            extract = text[:LIMIT]
            return {
                "state": data_hash,
                "error": "",
                "extract": extract,
                "status_code": response.status,
                "content_length": content_length,
                "timeout": timeout,
                "interval": self.config[CONF_INTERVAL],
            }
        except (
            TimeoutError,
            aiohttp.ClientError,
            aiohttp.http.HttpProcessingError,
        ) as err:
            error_message = str(err)[:LIMIT]  # Truncated error message
            _LOGGER.error(f"Error fetching data: {err}")
            return {
                "state": "unavailable",
                "error": error_message,
                "extract": "",
                "status_code": "error" if not response else response.status,
                "content_length": "error"
                if not response
                else response.headers.get("content-length", "error"),
                "timeout": timeout,
                "interval": self.config[CONF_INTERVAL],
            }
