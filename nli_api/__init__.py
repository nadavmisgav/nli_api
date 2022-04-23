"""Top-level package for National Library of Israel API."""

__author__ = """Nadav Misgav"""
__email__ = 'nadav.misgav@gmail.com'
__version__ = '0.1.0'

from .nli_api import get_nli_api
from .query import Queries, Query
from .api_ruleset import Where
