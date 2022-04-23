import sys

import pytest

sys.path.append('..')  # noqa: E402
from nli_api import Queries, Query
from nli_api.api_ruleset import Match, Where


class TestQuery:
    def test_init(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=False)
        assert query.query == 'test'
        assert query.exact is False
        assert query.where == Where.ANY

    def test_str(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=False)
        assert str(query) == f'{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_exact_str(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=True)
        assert str(query) == f'{Where.ANY.value},{Match.EXACT.value},test'


class TestQueries:
    def test_and(self):
        """Test one and"""
        queries = Queries()
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        assert str(queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_or(self):
        """Test one or"""
        queries = Queries()
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        assert str(queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_multiple_and(self):
        """Test multiple and"""
        queries = Queries()
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        assert str(
            queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_multiple_or(self):
        """Test multiple or"""
        queries = Queries()
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        assert str(
            queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_or_and(self):
        """Test or and"""
        queries = Queries()
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        assert str(
            queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'

        queries = Queries()
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        assert str(
            queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_multiple_or_and(self):
        """Test multiple or and"""
        queries = Queries()
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__or__(Query('test', where=Where.ANY, exact=False))
        queries = queries.__and__(Query('test', where=Where.ANY, exact=False))

        with pytest.warns(UserWarning):
            assert str(
                queries) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'
