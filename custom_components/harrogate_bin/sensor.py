"""GitHub sensor platform."""
# import re
from datetime import timedelta
import logging
import random
from typing import Any, Callable, Dict, Optional

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# import gidgethub
from aiohttp import ClientError
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_ID
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
import voluptuous as vol

from .const import ATTR_TEST

# from urllib import parse

# from gidgethub.aiohttp import GitHubAPI


_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ID): cv.positive_int,
    }
)


# LINK_RE = re.compile(
#     r"\<(?P<uri>[^>]+)\>;\s*" r'(?P<param_type>\w+)="(?P<param_value>\w+)"(,\s*)?'
# )
#
#
# def get_last_page_url(link: Optional[str]) -> Optional[str]:
#     # https://developer.github.com/v3/#pagination
#     # https://tools.ietf.org/html/rfc5988
#     if link is None:
#         return None
#     for match in LINK_RE.finditer(link):
#         if match.group("param_type") == "rel":
#             if match.group("param_value") == "last":
#                 return match.group("uri")
#     else:
#         return None


async def async_setup_platform(async_add_entities: Callable) -> None:
    """Set up the sensor platform."""
    # session = async_get_clientsession(hass)
    # github = GitHubAPI(session, "requester", oauth_token=config[CONF_ACCESS_TOKEN])
    sensors = [BinDaySensor("sensor_name")]
    async_add_entities(sensors, update_before_add=True)


class BinDaySensor(Entity):
    """Representation of a Bin Day sensor."""

    def __init__(self, name: str):
        super().__init__()
        self.attrs: Dict[str, Any] = {}
        self._name = name
        self._state = None
        self._available = True

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

    async def async_update(self):
        try:

            self.attrs[ATTR_TEST] = 3

            # Set state.
            self._state = 'abcdef'
            self._available = True
        except (ClientError, gidgethub.GitHubException):
            self._available = False
            _LOGGER.exception("Error retrieving data from GitHub.")

    # async def _get_total(self, url: str) -> int:
    #     """Get the total number of results for a GitHub resource URL.
    #
    #     GitHub's API doesn't provide a total count for paginated resources.  To get
    #     around that and to not have to request every page, we do a single request
    #     requesting 1 item per page.  Then we get the url for the last page in the
    #     response headers and parse the page number from there.  This page number is
    #     the total number of results.
    #     """
    #     api_url = f"{BASE_API_URL}{url}"
    #     params = {"per_page": 1, "state": "open"}
    #     headers = {"Authorization": self.github.oauth_token}
    #     async with self.github._session.get(
    #         api_url, params=params, headers=headers
    #     ) as resp:
    #         last_page_url = get_last_page_url(resp.headers.get("Link"))
    #         if last_page_url is not None:
    #             return int(dict(parse.parse_qsl(last_page_url))["page"])
    #     return 0
