from datetime import datetime

from bs4 import BeautifulSoup
import requests


class BinDay:

    def __init__(self, uprn: int):
        self.uprn = uprn

    def get_next_bin_day(self) -> tuple[datetime, str]:
        parsed_html = BeautifulSoup(self.get_page_html(), features="html.parser")
        rows = parsed_html.body.find_all('table', attrs={'class': 'hbcRounds'})

        timestamp = self.get_bin_day_from_row(rows[1], 0)
        if timestamp <= datetime.now():
            return self.get_bin_day_from_row(rows[1], 1), self.get_bin_type(rows[1], 1)

        return timestamp, self.get_bin_type(rows[1], 0)

    def get_page_html(self) -> str:
        return requests.get(
            url='https://secure.harrogate.gov.uk/inmyarea/Property/?uprn=' + self.uprn.__str__()
        ).content.__str__()

    @staticmethod
    def get_bin_day_from_row(row, cell) -> datetime:
        next_day = row.find_all('td')[cell].get_text().lstrip('\\r\\n').strip()[:15]
        return datetime.strptime(next_day + " 07", '%a %d %b %Y %H')

    @staticmethod
    def get_bin_type(row, cell) -> str:
        return row.find_all('th')[cell].get_text().lstrip('\\r\\n').strip()
