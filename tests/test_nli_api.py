#!/usr/bin/env python

"""Tests for `nli_api` package."""


import sys

from .conftest import API_KEY

sys.path.append('..')  # noqa: E402
from nli_api import get_nli_api


def test_get_nli_api():
    api = get_nli_api(API_KEY)
    assert api.session.params['api_key'] == API_KEY
