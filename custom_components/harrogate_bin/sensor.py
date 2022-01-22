"""GitHub sensor platform."""
# import re
from datetime import timedelta
import logging
from typing import Any, Callable, Dict, Optional

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# import gidgethub
from aiohttp import ClientError
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
import voluptuous as vol

from .const import ATTR_TYPE
from .parser import BinDay

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ID): cv.positive_int,
    }
)


async def async_setup_platform(
        hass: HomeAssistantType,
        config: ConfigType,
        async_add_entities: Callable,
        discovery_info: Optional[DiscoveryInfoType] = None
) -> None:
    """Set up the sensor platform."""
    sensors = [BinDaySensor(config[CONF_NAME], config[CONF_ID])]
    async_add_entities(sensors, update_before_add=True)


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
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    async def update(self):
        next_day = self._bin_day.get_next_bin_day()
        self.attrs[ATTR_TYPE] = next_day[1]

        # Set state.
        self._state = next_day[0]
        self._available = True
