"""Harrogate Bin Day Custom Component."""
import logging

from homeassistant import config_entries, core
from homeassistant.const import CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import entity_platform

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.positive_int,
        vol.Required(CONF_NAME): cv.string,
    }
)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the sensor platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    platform = entity_platform.async_get_current_platform(hass)
    platform.async_register_entity_service("bin_taken_out", {}, "mark_taken_out")

    return True


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Bin Day Custom component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True
