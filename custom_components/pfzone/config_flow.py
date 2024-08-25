"""Config flow for Urls monitor integration."""

import hashlib
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback

from .const import (
    CONF_HEADERS,
    CONF_INTERVAL,
    CONF_TIMEOUT,
    CONF_URL,
    DEFAULT_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
)
from .validations import validate_user_input

_LOGGER = logging.getLogger(__name__)


def _create_schema(options=None):
    return vol.Schema(
        {
            vol.Required(CONF_URL, default=options.get(CONF_URL, "")): str,
            vol.Optional(CONF_HEADERS, default=options.get(CONF_HEADERS, "")): str,
            vol.Required(
                CONF_INTERVAL,
                default=options.get(CONF_INTERVAL, DEFAULT_INTERVAL),
            ): int,
            vol.Required(
                CONF_TIMEOUT,
                default=options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT),
            ): int,
        }
    )


@config_entries.HANDLERS.register(DOMAIN)
class UrlsMonitorFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Urls monitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def _hash_url(self, url: str) -> str:
        """Generate a hash for the given URL."""
        return hashlib.sha256(url.encode()).hexdigest()

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            errors = validate_user_input(user_input)

            if not errors:
                url_hash = self._hash_url(user_input[CONF_URL])
                await self.async_set_unique_id(url_hash)
                self._abort_if_unique_id_configured(
                    updates={
                        CONF_HEADERS: user_input[CONF_HEADERS],
                        CONF_INTERVAL: user_input[CONF_INTERVAL],
                        CONF_TIMEOUT: user_input[CONF_TIMEOUT],
                    },
                    error=""
                )

                return self.async_create_entry(
                    title=user_input[CONF_URL], data=user_input
                )

        _LOGGER.debug(
            "Showing config form with user input: %s and errors: %s", user_input, errors
        )

        return self.async_show_form(
            step_id="user",
            data_schema=_create_schema({}),
            errors=errors or {},
        )

    async def async_step_reconfigure(self, user_input=None) -> ConfigFlowResult:
        """Handle the step for reconfiguration."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry
        config_entry = entry.data
        if config_entry is None:
            _LOGGER.error("Config entry not found in context")
            return self.async_abort(reason="missing_config_entry")

        _LOGGER.debug(
            "Reconfigure step initiated with current config: %s", config_entry[CONF_URL]
        )

        return self.async_show_form(
            step_id="user",
            data_schema=_create_schema(config_entry),
            errors={},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return UrlsMonitorOptionsFlowHandler(config_entry)


class UrlsMonitorOptionsFlowHandler(OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        errors = {}

        if user_input is not None:
            errors = validate_user_input(user_input)
            if not errors:
                return self.async_create_entry(title="", data=user_input)

            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_create_schema(errors),
            errors=errors,
        )
