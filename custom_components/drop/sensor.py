from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import async_get_current_platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        DropSensor(coordinator, "games_count", "Drop Games", "mdi:gamepad-variant"),
        DropSensor(coordinator, "users_count", "Drop Users", "mdi:account-multiple"),
        DropSensor(coordinator, "latest_game", "Drop Latest Added Game", "mdi:new-box"),
    ]

    async_add_entities(sensors)

class DropSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, data_key: str, name: str, icon: str):
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{coordinator.base_url}_{data_key}"

    @property
    def native_value(self):
        return self.coordinator.data.get(self._data_key)