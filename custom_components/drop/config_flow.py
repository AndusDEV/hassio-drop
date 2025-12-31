from homeassistant import config_entries
from homeassistant.const import CONF_URL, CONF_TOKEN
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN, CONF_BASE_URL, CONF_API_TOKEN

class DropConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if await self._async_test_connection(
                user_input[CONF_BASE_URL], user_input[CONF_API_TOKEN]
            ):
                return self.async_create_entry(title="Drop", data=user_input)
            errors["base"] = "cannot_connect"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_BASE_URL): str,
                vol.Required(CONF_API_TOKEN): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def _async_test_connection(self, base_url: str, api_token: str) -> bool:
        try:
            import aiohttp

            headers = {"Authorization": f"Bearer {api_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{base_url.rstrip('/')}/api/v1/admin/users", headers=headers, timeout=10
                ) as resp:
                    return resp.status == 200
        except Exception:
            return False