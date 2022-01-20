"""Tests for the sensor module."""
from custom_components.harrogate_bin.sensor import BinDaySensor


async def test_async_update_success(hass, aioclient_mock):
    """Tests a fully successful async_update."""
    sensor = BinDaySensor("name")
    await sensor.async_update()

    expected = {"test": 3}
    assert expected == sensor.attrs
    assert expected == sensor.device_state_attributes
    assert sensor.available is True
