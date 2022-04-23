"""
Query
"""
from __future__ import annotations

from typing import Union
from warnings import warn

from .api_ruleset import Match, Where

_UNSUPPORTED_FILTERS = [
    Where.START_DATE,
    Where.END_DATE,
    Where.LANGUAGE
]


class Query:
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

    def __and__(self, other: Union[Queries, Query]) -> Queries:
        """
        Return a Queries object with the current query and the other query.

        :param other: Union[Queries, Query] - The other query
        :return: Queries
        """
        if isinstance(other, Queries):
            return other.__and__(self)

        if isinstance(other, Query):
            queries = Queries()
            queries = queries.__and__(self)
            queries = queries.__and__(other)
            return queries

        raise TypeError(f"{type(other)} is not supported.")

    def __or__(self, other: Union[Queries, Query]) -> Queries:
        """
        Return a Queries object with the current query and the other query.

        :param other: Union[Queries, Query] - The other query
        :return: Queries
        """
        if isinstance(other, Queries):
            return other.__or__(self)

        if isinstance(other, Query):
            queries = Queries()
            queries = queries.__or__(self)
            queries = queries.__or__(other)
            return queries

        raise TypeError(f"{type(other)} is not supported.")

    def __str__(self):
        """
        Return a string representation of the query.
        """
        match = Match.EXACT.value if self.exact else Match.CONTAINS.value
        return f"{self.where.value},{match},{self.query}"


class Queries:
    """
    Represent multiple queries
    This will hold a list of lists of queries, where each innter list
    represents an AND group, and the outer list represents an OR group.

    :param queries: list[list[Query]] - List of queries

    """

    def __init__(self) -> None:
        self.queries = [[]]

    def __and__(self, other: Union[Queries, Query]) -> Queries:
        """
        Add a query to the AND group.

        :param other: Union[Queries, Query] - Query to add
        :return: Queries - Queries
        """
        if isinstance(other, Queries):
            self.queries[-1].extend(other.queries)
        elif isinstance(other, Query):
            self.queries[-1].append(other)
        else:
            raise TypeError(f"{type(other)} is not supported.")

        return self

    def __or__(self, other: Union[Queries, Query]) -> Queries:
        """
        Add a query to the OR group.

        :param other: Union[Queries, Query] - Query to add
        :return: Queries - Queries
        """
        if isinstance(other, Queries):
            self.queries.extend(other.queries)
        elif isinstance(other, Query):
            if len(self.queries[-1]) == 0:
                self.queries[-1].append(other)
            else:
                self.queries.append([other])
        else:
            raise TypeError(f"{type(other)} is not supported.")

        return self

    def __str__(self) -> str:
        """
        Return a string representation of the queries.
        """
        if len(self.queries) > 1 and any(len(q) > 1 for q in self.queries):
            warn("Not sure about the support for queries that are ANDed with OR queries.")

        and_queries = []
        for query_group in self.queries:
            and_queries.append(",AND;".join(str(q) for q in query_group))

        query = ",OR;".join(and_queries)

        return query
