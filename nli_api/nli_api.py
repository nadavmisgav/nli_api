"""Main module."""
from dataclasses import dataclass
from typing import Generator, List, Union
from warnings import warn

import requests

from .query import Queries, Query


@dataclass
class NLI_API_Response:
    id: str = ""
    date: str = ""
    type: str = ""
    recordid: str = ""
    title: str = ""
    source: str = ""
    language: str = ""
    identifier: str = ""
    linkToMarc: str = ""
    contributor: str = ""
    creator: str = ""
    subject: str = ""
    accessRights: str = ""
    publisher: str = ""
    format: str = ""
    non_standard_date: str = ""
    thumbnail: str = ""
    relation: str = ""
    download: str = ""


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

    def _get(self, url: str) -> dict:
        res = self.session.get(url)
        res.raise_for_status()
        return res.json()

    def search(self, query: Union[Query, Queries]) -> List[NLI_API_Response]:
        """
        Search for a query.

        :param query: Union[Query, Queries] - query to search for.
        :return: List[NLI_API_Response] - response from the API.
        """
        quoted = requests.utils.quote(str(query))
        url = self.BASE_URL.format(query=quoted)

        res = self._get(url)
        return list(self._parse_response(res))

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
