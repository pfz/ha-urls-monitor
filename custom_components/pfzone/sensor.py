"""Sensor platform for Urls monitor."""

import hashlib
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_URL, DOMAIN, HASH_SIZE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up Urls monitor sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([UrlsMonitorSensor(coordinator)], True)


class UrlsMonitorSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Urls monitor sensor."""

    def __init__(self, coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._attr_name = coordinator.config.get(CONF_URL, "Unknown URL")
        self._attr_unique_id = hashlib.md5(
            coordinator.config[CONF_URL].encode("utf-8")
        ).hexdigest()[:HASH_SIZE]

    @property
    def state(self) -> str:
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
