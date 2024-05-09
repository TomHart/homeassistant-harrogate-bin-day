from homeassistant.helpers import config_validation as cv, entity_platform, service


async def async_setup_entry(hass, entry):
    """Set up the media player platform for Sonos."""

    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service("bin_taken_out", {}, "mark_taken_out", )
