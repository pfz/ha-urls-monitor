"""Sensor platform for Urls monitor."""

import asyncio
from datetime import timedelta
import hashlib
import logging

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    CONF_HEADERS,
    CONF_INTERVAL,
    CONF_TIMEOUT,
    CONF_URL,
    DOMAIN,
    HASH_SIZE,
    LIMIT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Urls monitor sensor."""
    coordinator = UrlsMonitorCoordinator(hass, entry.data)
    await coordinator.async_refresh()

    async_add_entities([UrlsMonitorSensor(coordinator, entry)])


class UrlsMonitorCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the URL."""

    def __init__(self, hass, config):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=config[CONF_INTERVAL]),
        )
        self.config = config

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

            data_hash = self._generate_hash(text)
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
            aiohttp.ClientError,
            aiohttp.http.HttpProcessingError,
            asyncio.TimeoutError,
        ) as err:
            error_message = str(err)[:LIMIT]  # Truncated error message
            error_hash = self._generate_hash(error_message)
            _LOGGER.error(f"Error fetching data: {err}")
            return {
                "state": "unavailable",
                "error": error_message,
                "extract": "",
                "status_code": "error" if not response else response.status,
                "content_length": "error" if not response else response.headers.get("content-length", "error"),
                "timeout": timeout,
                "interval": self.config[CONF_INTERVAL],
            }

    @staticmethod
    def _generate_hash(data):
        """Generate a hash for a given data."""
        return hashlib.md5(data.encode("utf-8")).hexdigest()[:HASH_SIZE]


class UrlsMonitorSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Urls monitor sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = entry.data.get(CONF_URL, "Unknown URL")
        self._attr_unique_id = UrlsMonitorSensor._generate_unique_id(entry.data[CONF_URL])

    @staticmethod
    def _generate_unique_id(url):
        """Generate a unique ID for the sensor based on the URL."""
        return hashlib.md5(url.encode("utf-8")).hexdigest()[:HASH_SIZE]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("state", "unavailable")

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "error": self.coordinator.data.get("error", ""),
            "extract": self.coordinator.data.get("extract", ""),
            "status_code": self.coordinator.data.get("status_code", ""),
            "content_length": self.coordinator.data.get("content_length", ""),
            "timeout": self.coordinator.data.get("timeout", ""),
            "interval": self.coordinator.data.get("interval", ""),
        }
