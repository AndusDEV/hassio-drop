import logging
from datetime import datetime, timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_BASE_URL, CONF_API_TOKEN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    base_url = entry.data[CONF_BASE_URL].rstrip("/")
    api_token = entry.data[CONF_API_TOKEN]

    coordinator = DropDataUpdateCoordinator(hass, base_url, api_token)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

class DropDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, base_url: str, api_token: str):
        """Initialize."""
        self.base_url = base_url
        self.api_token = api_token
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                # Fetch users
                async with session.get(f"{self.base_url}/api/v1/admin/users", headers=headers) as resp:
                    resp.raise_for_status()
                    users_data = await resp.json()
                    users_count = len(users_data)

                # Fetch library
                async with session.get(f"{self.base_url}/api/v1/admin/library", headers=headers) as resp:
                    resp.raise_for_status()
                    library_data = await resp.json()
                    games = library_data.get("games", [])
                    games_count = len(games)

                    # Find latest added game
                    latest_game = "No games"
                    if games:
                        parsed_games = []
                        for item in games:
                            game_obj = item.get("game", {})
                            created_str = game_obj.get("created")
                            title = game_obj.get("mName") or "Unknown Game"
                            if created_str:
                                try:
                                    created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                                    parsed_games.append((created_dt, title))
                                except ValueError:
                                    continue

                        if parsed_games:
                            parsed_games.sort(reverse=True)
                            latest_game = parsed_games[0][1]

            return {
                "users_count": users_count,
                "games_count": games_count,
                "latest_game": latest_game,
            }
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"API error: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error fetching Drop data: %s", err)
            raise UpdateFailed(f"Unexpected error: {err}") from err