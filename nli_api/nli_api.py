"""Main module."""
import asyncio
from dataclasses import dataclass
from itertools import chain
from typing import Generator, List, Optional, Union
from warnings import warn

import requests

from .api_ruleset import Errors
from .query import Query


@dataclass
class NLI_API_Response:
    id: str
    date: str
    type: str
    recordid: str
    title: str
    source: str
    language: str
    identifier: str
    linkToMarc: str
    contributor: str
    creator: str
    subject: str
    accessRights: str
    publisher: str
    format: str
    non_standard_date: str
    thumbnail: str
    relation: str
    download: str


class NLI_API:
    """
    NLI_API class.
    """

    BASE_URL = "https://api.nli.org.il/openlibrary/search?query={query}"

    def __init__(self, session: requests.Session):
        """
        Initialize NLI_API class.

        :param session: requests.Session - requests session that attaches an API key to all requests.
        """
        self.session = session

    def _get(self, url: str) -> requests.Response:
        res = self.session.get(url)
        res.raise_for_status()
        return res

    def _api_get(self, url: str) -> requests.Response:
        res = self._get(url)
        if "errors" in res.headers:
            if Errors.INVALID_PAGE.value in res.headers["errors"]:
                raise FileExistsError("Page does not exist.")

        return res

    def _api_query_page(self, encoded_query: str, page: Optional[int] = None) -> requests.Response:
        """
        Get a response from the API.

        :param encoded_query: str - encoded_query to search for.
        :param page: Optional[int] - page number to search for.
        :return: List[NLI_API_Response] - response from the API.
        """
        quoted = requests.utils.quote(encoded_query)
        url = self.BASE_URL.format(query=quoted)
        if page:
            url += f"&result_page={page}"

        res = self._api_get(url)
        return res

    def _get_page(self, encoded_query: str, page: Optional[int] = None) -> List[NLI_API_Response]:
        """
        Get a single page of a query.

        :param encoded_query: str - encoded_query to search for.
        :param page: Optional[int] - page number to search for.
        :return: NLI_API_Response - response from the API.
        """
        res = self._api_query_page(encoded_query, page=page)
        return list(self._parse_response(res.json()))

    def _get_many_pages(self, encoded_query: str, num_pages: int, start_page: int = 1) -> List[NLI_API_Response]:
        """
        Get many pages in an asyncio loop.

        :param encoded_query: str - encoded_query to search for.
        :param num_pages: int - number of pages to search for.
        :param start_page: int - page number to start from.
        :return: List[NLI_API_Response] - response from the API.
        """

        loop = asyncio.get_event_loop()
        funcs = [loop.run_in_executor(None, self._get_page, encoded_query, i)
                 for i in range(start_page, start_page + num_pages)]
        res = loop.run_until_complete(asyncio.gather(*funcs))

        return list(chain.from_iterable(res))

    def get_num_articles(self, query: Union[str, Query]) -> int:
        """
        Get the number of articles from the API.

        :param query: Union[str, Query] - query to search for.
        :return: int - number of articles.
        """
        if isinstance(query, str):
            query = Query(query)

        res = self._api_query_page(str(query))
        return int(res.headers["totalarticles"])

    def search(self, query: Union[str, Query], page: Optional[int] = None, all_pages: bool = False) -> List[NLI_API_Response]:
        """
        Search for a query.

        :param query: Union[str, Query] - query to search for.
        :param page: Optional[int] - page number to search for. Defaults to first page.
        :param all_pages: bool - if True, return all pages of results.
        :return: List[NLI_API_Response] - response from the API.
        """

        if page and all_pages:
            raise ValueError("Cannot specify both page and all_pages.")

        num_articles = self.get_num_articles(query)
        num_pages = num_articles // 50 + 1

        if isinstance(query, str):
            query = Query(query)
        query_str = str(query)

        if all_pages:
            return self._get_many_pages(query_str, num_pages)

        return self._get_page(query_str, page=page)

    @staticmethod
    def _parse_response(response: dict) -> Generator[NLI_API_Response, None, None]:
        """
        Parse the response from the API.

        :param response: dict - response from the API.
        :return: Generator[NLI_API_Response, None, None] - parsed response.
        """
        def _parse_key(obj: dict, key: str) -> str:
            _prefix = "http://purl.org/dc/elements/1.1/"

            try:
                inner_obj = obj[f"{_prefix}{key}"][0]
                if "@value" in inner_obj:
                    return inner_obj["@value"]
                if "@id" in inner_obj:
                    return inner_obj["@id"]

                warn(f"Unknown keys: {list(inner_obj.keys())}")
            except KeyError:
                return ""

        for res in response:
            yield NLI_API_Response(
                id=res.get("@id", ""),
                date=_parse_key(res, "date"),
                type=_parse_key(res, "type"),
                recordid=_parse_key(res, "recordid"),
                title=_parse_key(res, "title"),
                source=_parse_key(res, "source"),
                language=_parse_key(res, "language"),
                identifier=_parse_key(res, "identifier"),
                linkToMarc=_parse_key(res, "linkToMarc"),
                contributor=_parse_key(res, "contributor"),
                creator=_parse_key(res, "creator"),
                subject=_parse_key(res, "subject"),
                accessRights=_parse_key(res, "accessRights"),
                publisher=_parse_key(res, "publisher"),
                format=_parse_key(res, "format"),
                non_standard_date=_parse_key(res, "non_standard_date"),
                thumbnail=_parse_key(res, "thumbnail"),
                relation=_parse_key(res, "relation"),
                download=_parse_key(res, "download"),
            )


def get_nli_api(api_token: str) -> NLI_API:
    """
    Returns NLI_API class.

    : param api_key: NLI API key generated from `https: // api.nli.org.il/signup /`.
    """
    session = requests.Session()
    session.params = {'api_key': api_token}
    return NLI_API(session)
