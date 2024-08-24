"""Config flow for Urls monitor integration."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_HEADERS, CONF_INTERVAL, CONF_TIMEOUT, CONF_URL, DOMAIN, DEFAULT_INTERVAL, DEFAULT_TIMEOUT
from .validations import is_valid_headers, is_valid_url


@config_entries.HANDLERS.register(DOMAIN)
class UrlsMonitorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Urls monitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            if not is_valid_url(user_input[CONF_URL]):
                errors[CONF_URL] = "invalid_url"

            if user_input.get(CONF_HEADERS) and not is_valid_headers(
                user_input[CONF_HEADERS]
            ):
                errors[CONF_HEADERS] = "invalid_headers"

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_URL], data=user_input
                )

        return self._show_config_form(user_input, errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return UrlsMonitorOptionsFlowHandler(config_entry)

    def _show_config_form(self, user_input=None, errors=None):
        """Show the configuration form to edit location data."""
        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=user_input.get(CONF_URL, "")): str,
                    vol.Optional(
                        CONF_HEADERS, default=user_input.get(CONF_HEADERS, "")
                    ): str,
                    vol.Required(
                        CONF_INTERVAL, default=user_input.get(CONF_INTERVAL, DEFAULT_INTERVAL)
                    ): int,
                    vol.Required(
                        CONF_TIMEOUT, default=user_input.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
                    ): int,
                }
            ),
            errors=errors or {},
        )


class UrlsMonitorOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            if not is_valid_url(user_input[CONF_URL]):
                errors[CONF_URL] = "invalid_url"

            if user_input.get(CONF_HEADERS) and not is_valid_headers(
                user_input[CONF_HEADERS]
            ):
                errors[CONF_HEADERS] = "invalid_headers"

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        return self._show_options_form(errors)

    def _show_options_form(self, errors=None):
        """Show the configuration form to edit options."""
        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=options.get(CONF_URL, "")): str,
                    vol.Optional(
                        CONF_HEADERS, default=options.get(CONF_HEADERS, "")
                    ): str,
                    vol.Required(
                        CONF_INTERVAL, default=options.get(CONF_INTERVAL, 60)
                    ): int,
                    vol.Required(
                        CONF_TIMEOUT, default=options.get(CONF_TIMEOUT, 10)
                    ): int,
                }
            ),
            errors=errors or {},
        )
