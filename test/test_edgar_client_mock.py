import unittest.mock as mock

import pandas as pd

import helpers.unit_test as hut
import p1_data_client_python.edgar_client as p1_edg
import p1_data_client_python.exceptions as p1_exc

SEARCH_ROW_EXAMPLE = {
    "name": "qweqwe",
    "commodity": "qweqweqwe",
    "payload_id": "asdasd",
    "business_category": "asdasd",
    "country": "asdasd",
    "frequency": "asdasd",
    "unit": "zxc",
    "start_date": "zxcff",
}


class PayloadGoodResponseMock:
    status_code = 200

    @staticmethod
    def json() -> dict:
        return {
            "count": 2,
            "data": [
                        {
                            "form_uuid": "85de174e-bad7-4d0a-a498-673293c8e318",
                            "filing_url": "https://www.sec.gov/Archives/edgar/data/1357204/000135720420000020/0001357204-20-000020-index.html",
                            "form_publication_timestamp": "2020-04-30T06:01:44-04:00",
                            "filing_date": "2020-04-30T00:00:00",
                            "creation_timestamp": "2020-12-04T01:21:37.131475+00:00",
                            "cik": 1357204,
                            "ticker": "DNKN",
                            "gvkey": "174222",
                            "item_name": "SALE_QUARTER",
                            "form_table_row_name": "Total revenues",
                            "item_value": 323.144,
                            "compustat_timestamp": "2020-04-30T16:00:00-04:00",
                            "period_of_report": "NA",
                            "compustat_coifnd_id": "NA"
                        },
                        {
                            "form_uuid": "85de174e-bad7-4d0a-a498-673293c8e318",
                            "filing_url": "https://www.sec.gov/Archives/edgar/data/1357204/000135720420000020/0001357204-20-000020-index.html",
                            "form_publication_timestamp": "2020-04-30T06:01:44-04:00",
                            "filing_date": "2020-04-30T00:00:00",
                            "creation_timestamp": "2020-12-04T01:21:37.131475+00:00",
                            "cik": 1357204,
                            "ticker": "DNKN",
                            "gvkey": "174222",
                            "item_name": "TXDITC_QUARTER",
                            "form_table_row_name": "Deferred income taxes, net",
                            "item_value": 202.175,
                            "compustat_timestamp": "2020-04-30T16:00:00-04:00",
                            "period_of_report": "NA",
                            "compustat_coifnd_id": "NA"
                        }
            ]
        }


class CikGoodResponseMock:
    status_code = 200

    @staticmethod
    def json() -> dict:
        return {"data": ["123"]}


class MessyResponseMock:
    status_code = 200

    @staticmethod
    def json() -> dict:
        return {"message": "strange_message"}


class TestEdgarPythonClientMock(hut.TestCase):
    def setUp(self) -> None:
        self.client = p1_edg.EdgarClient(token="goo token")
        super().setUp()

    @mock.patch("requests.Session.request")
    def test_payload(self, mock_request) -> None:
        # test on UnauthorizedException
        mock_request.return_value = mock.Mock(status_code=401)
        with self.assertRaises(p1_exc.UnauthorizedException):
            self.client.get_payload("8-K", 123)
        # test on good response
        mock_request.return_value = PayloadGoodResponseMock()
        self.assertIsInstance(self.client.get_payload("8-K", 123), pd.DataFrame)

    @mock.patch("requests.Session.request")
    def test_get_cik_(self, mock_request) -> None:
        # test on UnauthorizedException
        mock_request.return_value = mock.Mock(status_code=401)
        with self.assertRaises(p1_exc.UnauthorizedException):
            self.client.get_cik(gvk=123, gvk_date="2020-01-01")
        # test on good response
        mock_request.return_value = CikGoodResponseMock()
        self.assertIsInstance(
            self.client.get_cik(gvk=123, gvk_date="2020-01-01"),
            pd.DataFrame,
        )
