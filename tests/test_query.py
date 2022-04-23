import sys

import pytest

sys.path.append('..')  # noqa: E402
from nli_api import Query
from nli_api.api_ruleset import Match, Where


class TestQuery:
    def test_init(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=False)
        q = query._queries[0][0]
        assert q.query == 'test'
        assert q.exact is False
        assert q.where == Where.ANY

    def test_str(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=False)
        assert str(query) == f'{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_exact_str(self):
        """Test that the class can be initialized."""
        query = Query('test', where=Where.ANY, exact=True)
        assert str(query) == f'{Where.ANY.value},{Match.EXACT.value},test'

    def test_multiple_and(self):
        """Test multiple and"""
        query = Query('test', where=Where.ANY, exact=False)
        query.and_('test', where=Where.ANY, exact=False)
        assert str(
            query) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_multiple_or(self):
        """Test multiple or"""
        query = Query('test', where=Where.ANY, exact=False)
        query.or_('test', where=Where.ANY, exact=False)
        assert str(
            query) == f'{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_or_and(self):
        """Test or and"""
        query = Query('test', where=Where.ANY, exact=False)
        query.and_('test', where=Where.ANY, exact=False)
        assert str(
            query) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'

        query = Query('test', where=Where.ANY, exact=False)
        query.or_('test', where=Where.ANY, exact=False)
        assert str(
            query) == f'{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test'

    def test_multiple_or_and(self):
        """Test multiple or and"""
        query = Query('test', where=Where.ANY, exact=False) \
            .and_('test', where=Where.ANY, exact=False) \
            .or_('test', where=Where.ANY, exact=False) \
            .and_('test', where=Where.ANY, exact=False)

        with pytest.warns(UserWarning):
            assert str(
                query) == f'{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test,OR;{Where.ANY.value},{Match.CONTAINS.value},test,AND;{Where.ANY.value},{Match.CONTAINS.value},test'
