import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

from custom_components.harrogate_bin.const import ATTR_TYPE, ATTR_NOTE, ATTR_HOURS_UNTIL, ATTR_TAKEN_OUT
from custom_components.harrogate_bin.parser import BinDay
from custom_components.harrogate_bin.sensor import BinDaySensor


class TestBinDaySensor(unittest.TestCase):

    @patch('custom_components.harrogate_bin.sensor.BinDay')
    def test_update_method(self, mock_bin_day):
        # Mocking the BinDay class
        mock_bin_day_instance = mock_bin_day.return_value
        state_date = datetime.now() + timedelta(days=1)
        mock_bin_day_instance.get_next_bin_day.return_value = (state_date, "Recycling", "Bank Holiday")

        # Creating a BinDaySensor instance
        sensor = BinDaySensor("Test Sensor", "123456")  # Replace "123456" with your desired UPRN

        # Calling the update method
        sensor.update()

        # Assertions
        assert sensor.state == state_date
        assert sensor.available is True
        assert sensor.extra_state_attributes[ATTR_TYPE] is 'Recycling'
        assert sensor.extra_state_attributes[ATTR_HOURS_UNTIL] >= 23
        assert sensor.extra_state_attributes[ATTR_NOTE] is 'Bank Holiday'

    @patch('custom_components.harrogate_bin.sensor.BinDay')
    def test_update_resets_taken_out(self, mock_bin_day):
        # Mocking the BinDay class
        mock_bin_day_instance = mock_bin_day.return_value
        state_date = datetime.now() + timedelta(days=1)
        mock_bin_day_instance.get_next_bin_day.return_value = (state_date, "Recycling", '')

        # Creating a BinDaySensor instance
        sensor = BinDaySensor("Test Sensor", "123456")  # Replace "123456" with your desired UPRN

        # Default False
        sensor.update()
        assert sensor.extra_state_attributes[ATTR_TAKEN_OUT] is False

        # Change to True, doesn't reset if date hasn't changed
        sensor.extra_state_attributes[ATTR_TAKEN_OUT] = True
        sensor.update()
        assert sensor.extra_state_attributes[ATTR_TAKEN_OUT] is True

        # Resets when date changes
        state_date = datetime.now() + timedelta(days=2)
        mock_bin_day_instance.get_next_bin_day.return_value = (state_date, "Recycling", '')
        sensor.update()
        assert sensor.extra_state_attributes[ATTR_TAKEN_OUT] is False
