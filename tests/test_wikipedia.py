from unittest.mock import Mock

import click
import pytest

from generalized_hough import wikipedia


def test_random_page_returns_page(mock_requests_get):
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


def test_trigger_typeguard(mock_requests_get):
    import json

    data = json.loads('{ "language": "en" }')
    wikipedia.random_page(language=data["language"])
