import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from custom_components.harrogate_bin.parser import BinDay


class TestBinDay(unittest.TestCase):

    @patch('requests.get')
    def test_get_next_bin_day(self, mock_requests_get):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        formatted_date = tomorrow.strftime('%a %d %b %Y')

        # Mocking the requests.get method
        mock_response = MagicMock()
        mock_response.content = '<html><body><table class="hbcRounds"><tbody><tr ' \
                                'class="rmRowGarden"><th>Garden</th><td>{} <span class="hbcBH">Changed due to a bank ' \
                                'holiday</span></td></tr></tbody></table></body></html>'.format(formatted_date)
        mock_requests_get.return_value = mock_response

        bin_day = BinDay(123456)

        timestamp, bin_type, note = bin_day.get_next_bin_day()

        assert timestamp.strftime('%a %d %b %Y %H:%M') == formatted_date + ' 07:00'
        assert bin_type == 'Garden'
        assert note is None


    @patch('requests.get')
    def test_get_next_bin_day_note(self, mock_requests_get):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        formatted_date = tomorrow.strftime('%a %d %b %Y')

        # Mocking the requests.get method
        mock_response = MagicMock()
        mock_response.content = '<html><body><table class="hbcRounds"><tbody><tr ' \
                                'class="rmRowGarden"><th>Garden</th><td>{} <span class="hbcBH">Changed due to a bank ' \
                                'holiday</span></td></tr></tbody></table></body></html>'.format(formatted_date)
        mock_requests_get.return_value = mock_response

        bin_day = BinDay(123456)

        timestamp, bin_type, note = bin_day.get_next_bin_day()

        assert timestamp.strftime('%a %d %b %Y %H:%M') == formatted_date + ' 07:00'
        assert bin_type == 'Garden'
        assert note == 'Changed due to a bank holiday'

    @patch('requests.get')
    def test_get_next_bin_day_following_day(self, mock_requests_get):
        today = datetime.now()
        yesterday = (today - timedelta(days=1)).strftime('%a %d %b %Y')
        tomorrow = (today - timedelta(days=1)).strftime('%a %d %b %Y')

        # Mocking the requests.get method
        mock_response = MagicMock()
        mock_response.content = '<html><body><table class="hbcRounds"><tbody><tr ' \
                                'class="rmRowGarden"><th>Garden</th><td>{}</td></tr><tr ' \
                                'class="rmRowGarden"><th>Refuse</th><td>{}' \
                                '</td></tr></tbody></table></body></html>'.format(yesterday, tomorrow)
        mock_requests_get.return_value = mock_response

        bin_day = BinDay(123456)

        timestamp, bin_type = bin_day.get_next_bin_day()

        assert timestamp.strftime('%a %d %b %Y %H:%M') == tomorrow + ' 07:00'
        assert bin_type == 'Refuse'
