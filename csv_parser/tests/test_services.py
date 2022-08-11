from unittest import TestCase
from csv_parser import services


class CSVParserServicesTestCase(TestCase):
    def test_get_spreadsheet_id_from_url(self):
        url = 'https://docs.google.com/spreadsheets/d/1hPs5MNwbIEOPsAI0BV9ccpNc-uuiK5GtDk6VFlhHv9g/edit#gid=76646525/export'
        valid_url = '1hPs5MNwbIEOPsAI0BV9ccpNc-uuiK5GtDk6VFlhHv9g'
        self.assertEqual(
            services.get_spreadsheet_id_from_url(url),
            valid_url,
        )
