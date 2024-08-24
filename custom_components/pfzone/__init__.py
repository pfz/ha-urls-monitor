"""The URL Monitor integration."""

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

DOMAIN = "url_monitor"
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the URL Monitor component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up URL Monitor from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True
