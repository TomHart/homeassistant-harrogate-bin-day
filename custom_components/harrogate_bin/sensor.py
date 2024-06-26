"""Bin Day sensor platform."""

from datetime import datetime, timedelta
import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_ID, CONF_NAME, CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity import Entity
import voluptuous as vol

from .const import ATTR_HOURS_UNTIL, ATTR_TYPE, DOMAIN, ATTR_NOTE, ATTR_TAKEN_OUT
from .parser import BinDay

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,
        vol.Required(CONF_ID): cv.positive_int,
        vol.Required(CONF_NAME): cv.string,
    }
)


async def async_setup_entry(
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    sensors = [BinDaySensor(config[CONF_NAME], config[CONF_ID])]
    async_add_entities(sensors, update_before_add=True)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service("bin_taken_out", {}, "mark_taken_out")
    platform.async_register_entity_service("bin_reset_taken_out", {}, "reset_taken_out")


class BinDaySensor(Entity):
    """Representation of a Bin Day sensor."""

    def __init__(self, name: str, uprn: str):
        super().__init__()
        self.attrs: Dict[str, Any] = {}
        self._name = name
        self._state = None
        self._available = True
        self._bin_day = BinDay(int(uprn))

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.name

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @staticmethod
    def _get_hours_until(date: datetime) -> int:
        return divmod((date - datetime.now()).total_seconds(), 3600)[0]

    def update(self):
        next_day = self._bin_day.get_next_bin_day()
        self.attrs[ATTR_TYPE] = next_day[1]
        self.attrs[ATTR_HOURS_UNTIL] = self._get_hours_until(next_day[0])
        self.attrs[ATTR_NOTE] = next_day[2] or None

        if self._state != next_day[0]:
            self.attrs[ATTR_TAKEN_OUT] = False

        # Set state.
        self._state = next_day[0]
        self._available = True

    def mark_taken_out(self):
        self.attrs[ATTR_TAKEN_OUT] = True

    def reset_taken_out(self):
        self.attrs[ATTR_TAKEN_OUT] = False
