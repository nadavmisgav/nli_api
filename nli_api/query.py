"""
Query
"""
from __future__ import annotations

from warnings import warn

from .api_ruleset import Match, Where

_UNSUPPORTED_FILTERS = [
    Where.START_DATE,
    Where.END_DATE,
    Where.LANGUAGE
]


class _Query:
    """
    Reperesent a single query.

    :param query: str - String to search
    :param where: Where - Where to search
    :param exact: bool - Whether to search for exact match
    """

    def __init__(self, query: str, where: Where = Where.ANY, exact: bool = False):
        """
        Initialize Query class.

        :param query: str - String to search
        :param where: Where - Where to search
        :param exact: bool - Whether to search for exact match
        """
        if where in _UNSUPPORTED_FILTERS:
            raise NotImplementedError(
                "{where.value} filtering is not implemented yet.")

        self.exact = exact
        self.query = query
        self.where = where

    def __str__(self):
        """
        Return a string representation of the query.
        """
        match = Match.EXACT.value if self.exact else Match.CONTAINS.value
        return f"{self.where.value},{match},{self.query}"


class Query:
    """
    Represent multiple queries
    This will hold a list of lists of queries, where each innter list
    represents an AND group, and the outer list represents an OR group.

    :param queries: list[list[_Query]] - List of queries

    """

    def __init__(self, query: str, where: Where = Where.ANY, exact: bool = False):
        q = _Query(query, where, exact)
        self._queries = [[q]]

    def and_(self, query: str, where: Where = Where.ANY, exact: bool = False) -> Query:
        """
        Add a query to the AND group.

        :param query: str - String to search
        :param where: Where - Where to search
        :param exact: bool - Whether to search for exact match
        :return: Query - Query
        """

        q = _Query(query, where, exact)
        self._queries[-1].append(q)
        return self

    def or_(self, query: str, where: Where = Where.ANY, exact: bool = False) -> Query:
        """
        Add a query to the OR group.

        :param query: str - String to search
        :param where: Where - Where to search
        :param exact: bool - Whether to search for exact match
        :return: Query - Query
        """
        q = _Query(query, where, exact)
        self._queries.append([q])
        return self

    def __str__(self) -> str:
        """
        Return a string representation of the queries.
        """
        if len(self._queries) > 1 and any(len(q) > 1 for q in self._queries):
            warn("Not sure about the support for queries that are ANDed with OR queries.")

        and_queries = []
        for query_group in self._queries:
            and_queries.append(",AND;".join(str(q) for q in query_group))

        query = ",OR;".join(and_queries)

        return query
