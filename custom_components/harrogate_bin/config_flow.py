import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.positive_int,
        vol.Required(CONF_NAME): cv.string,
    }
)

# def validate_path(path: str) -> None:
#     """Validates a GitHub repo path.
#
#     Raises a ValueError if the path is invalid.
#     """
#     if len(path.split("/")) != 2:
#         raise ValueError
#
#
# async def validate_auth(access_token: str, hass: core.HomeAssistant) -> None:
#     """Validates a GitHub access token.
#
#     Raises a ValueError if the auth token is invalid.
#     """
#     session = async_get_clientsession(hass)
#     gh = GitHubAPI(session, "requester", oauth_token=access_token)
#     try:
#         await gh.getitem("repos/home-assistant/core")
#     except BadRequest:
#         raise ValueError


class BinDayCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Bin Day Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.data = user_input

        return self.async_show_form(
            step_id="home", data_schema=PLATFORM_SCHEMA, errors=errors
        )
