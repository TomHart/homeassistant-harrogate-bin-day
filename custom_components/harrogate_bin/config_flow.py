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


class BinDayCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Bin Day Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title="Bin Day", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=PLATFORM_SCHEMA, errors=errors
        )
