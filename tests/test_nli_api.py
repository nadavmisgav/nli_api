#!/usr/bin/env python

"""Tests for `nli_api` package."""


import sys

sys.path.append('..')  # noqa: E402
from nli_api import get_nli_api


def test_get_nli_api():
    api = get_nli_api("123456")
    assert api.session.params['api_key'] == "123456"
