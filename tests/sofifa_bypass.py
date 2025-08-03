"""
Tests Sofifa.com accessibility using curl_cffi with spoofed browser headers.
"""

import curl_cffi  # third-party
from app.utils.headers import HEADERS  # first-party

URL = "https://sofifa.com/players"


def test_sofifa_status_code():
    """
    Ensure that Sofifa.com responds with HTTP 200 when accessed with headers.
    """
    response = curl_cffi.get(URL, headers=HEADERS, impersonate="chrome")
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
