from unittest.mock import Mock, patch

import pytest

from mbox_converter.base import (
    MboxConverter,
    parse_date,
    decode_mime_header,
    clean_content,
    extract_emails,
)
from mbox_converter.base import NAME
from mbox_converter.config import ConfigParameterManager


# install pytest and pytest-mock and run tests manually from the terminal:
# pip install pytest pytest-mock
# pytest


# ------------------------------
# Tests for individual functions
# ------------------------------


def test_base():
    assert NAME == "mbox_converter"


def test_parse_date_valid():
    date_str = "Mon, 05 Jun 2023 12:34:56 +0000"
    assert parse_date(date_str, "%Y-%m-%d") == "2023-06-05"


def test_parse_date_invalid():
    assert parse_date("Invalid date", "%Y-%m-%d") is None


def test_decode_mime_header_simple():
    assert decode_mime_header("Test Subject äöü?ß") == "Test Subject äöü?ß"


def test_decode_mime_header_encoded():
    encoded = "=?UTF-8?B?VGVzdCDDvGJlcg==?="  # "Test über"
    assert decode_mime_header(encoded) == "Test über"


def test_clean_content_html():
    html = b"<html><body><p>Hello <b>World</b></p></body></html>"
    assert clean_content(html).strip() == "Hello World"


def test_extract_emails_basic():
    field = "John Doe <john@example.com>, jane.doe@example.org"
    assert extract_emails(field) == ["jane.doe@example.org", "john@example.com"]


# ------------------------------
# Tests for MboxParser class
# ------------------------------


@pytest.fixture
def mock_email():
    email = Mock()
    email.get = lambda x, d=None: {
        "from": "Alice <alice@example.com>",
        "to": "Bob <bob@example.com>",
        "date": "Mon, 05 Jun 2023 12:34:56 +0000",
        "subject": "Test Subject",
    }.get(x, d)
    email.walk.return_value = [
        Mock(
            get_payload=lambda decode: b"Hello\nReply",
            get_content_maintype=lambda: "text",
        )
    ]
    return email


def test_build_txt_output(mock_email):
    config = ConfigParameterManager()
    parser = MboxConverter(config)
    output = parser.build_txt_output(mock_email)
    assert "From: alice@example.com" in output
    assert "To: bob@example.com" in output
    assert "Subject: Test Subject" in output
    assert "Hello" in output


def test_build_csv_output(mock_email):
    config = ConfigParameterManager()
    parser = MboxConverter(config)
    date_str = "2023-06-05"
    fields = parser.build_csv_output(mock_email, date_str)
    assert len(fields) == 5  # From, To, Date, Subject, Content
    assert "alice@example.com" in fields[0]
    assert "bob@example.com" in fields[1]
    assert "2023-06-05" in fields[2]
    assert "Test Subject" in fields[3]


@patch("mbox_converter.base.mailbox.mbox")
@patch("mbox_converter.base.open", create=True)
def test_parse_creates_output(mock_open, mock_mbox, mocker):
    fake_email = Mock()
    fake_email.get.side_effect = lambda x, d=None: {
        "from": "a@a.com",
        "to": "b@b.com",
        "date": "Mon, 05 Jun 2023 12:34:56 +0000",
        "subject": "Test",
    }.get(x, d)
    fake_email.walk.return_value = [
        Mock(get_payload=lambda decode: b"Text", get_content_maintype=lambda: "text")
    ]

    mock_mbox.return_value = [fake_email]
    mock_file = mock_open.return_value.__enter__.return_value

    config = ConfigParameterManager()
    parser = MboxConverter(config)
    parser.convert()

    assert mock_open.called
    # assert mock_file.write.called


def test_max_days_split(mocker):
    """Test splitting by max_days across multiple mock emails."""
    email1 = Mock()
    email2 = Mock()
    email1.get.side_effect = email2.get.side_effect = lambda x, d=None: {
        "from": "a@a.com",
        "to": "b@b.com",
        "date": "Mon, 01 Jan 2024 12:00:00 +0000",
        "subject": "First",
    }.get(x, d)
    email2.get = lambda x, d=None: {
        "from": "a@a.com",
        "to": "b@b.com",
        "date": "Thu, 04 Jan 2024 12:00:00 +0000",  # 3 days later
        "subject": "Second",
    }.get(x, d)
    email1.walk.return_value = email2.walk.return_value = [
        Mock(get_payload=lambda decode: b"Text", get_content_maintype=lambda: "text")
    ]

    mocker.patch("mbox_converter.base.mailbox.mbox", return_value=[(email1), (email2)])
    mock_open = mocker.patch("mbox_converter.base.open", mocker.mock_open())
    config = ConfigParameterManager()
    config.max_days = 2
    parser = MboxConverter(config)
    parser.convert()

    assert mock_open.call_count >= 2  # Should open two output files
