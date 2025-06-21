import logging
import aiohttp
import voluptuous as vol
from typing import Any

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_UGREEN_HOST,
    CONF_UGREEN_PORT,
    CONF_AUTH_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_USE_HTTPS,
    CONF_VERIFY_SSL,
)
from .api import UgreenApiClient

_LOGGER = logging.getLogger(__name__)

class UgreenNasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UGREEN NAS."""
    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            _LOGGER.info("[UGREEN NAS] Received user input: %s", user_input)

            try:
                api = UgreenApiClient(
                    ugreen_nas_host=user_input[CONF_UGREEN_HOST],
                    ugreen_nas_port=int(user_input[CONF_UGREEN_PORT]),
                    auth_port=int(user_input[CONF_AUTH_PORT]),
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    use_https=user_input.get(CONF_USE_HTTPS, False),
                    verify_ssl=user_input.get(CONF_VERIFY_SSL, False),
                )

                async with aiohttp.ClientSession() as session:
                    success = await api.authenticate(session)
                    if not success:
                        errors["base"] = "invalid_auth"
                    else:
                        _LOGGER.info("[UGREEN NAS] Successfully authenticated")
                        return self.async_create_entry(title="UGREEN NAS", data={
                            CONF_UGREEN_HOST: user_input[CONF_UGREEN_HOST],
                            CONF_UGREEN_PORT: user_input[CONF_UGREEN_PORT],
                            CONF_AUTH_PORT: user_input[CONF_AUTH_PORT],
                            CONF_USERNAME: user_input[CONF_USERNAME],
                            CONF_PASSWORD: user_input[CONF_PASSWORD],
                            CONF_USE_HTTPS: user_input.get(CONF_USE_HTTPS, False),
                            CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL, False),
                        })

            except Exception as e:
                _LOGGER.exception("[UGREEN NAS] Connection/authentication failed: %s", e)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_UGREEN_HOST): str,
                vol.Required(CONF_UGREEN_PORT, default=9443): int,
                vol.Required(CONF_AUTH_PORT, default=4115): int,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_USE_HTTPS, default=False): bool,
                vol.Optional(CONF_VERIFY_SSL, default=False): bool,
            }),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        _LOGGER.debug("[UGREEN NAS] Starting options flow for config entry: %s", config_entry.entry_id)
        return UgreenNasOptionsFlowHandler(config_entry)


class UgreenNasOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle UGREEN NAS options."""
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            _LOGGER.info("[UGREEN NAS] Options updated: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_UGREEN_HOST, default=current.get(CONF_UGREEN_HOST, "")): str,
                vol.Optional(CONF_UGREEN_PORT, default=current.get(CONF_UGREEN_PORT, 9443)): int,
                vol.Optional(CONF_AUTH_PORT, default=current.get(CONF_AUTH_PORT, 4115)): int,
                vol.Optional(CONF_USERNAME, default=current.get(CONF_USERNAME, "")): str,
                vol.Optional(CONF_PASSWORD, default=current.get(CONF_PASSWORD, "")): str,
                vol.Optional(CONF_USE_HTTPS, default=current.get(CONF_USE_HTTPS, False)): bool,
                vol.Optional(CONF_VERIFY_SSL, default=current.get(CONF_VERIFY_SSL, False)): bool,
            }),
        )
