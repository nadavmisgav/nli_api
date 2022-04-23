from enum import Enum


class Match(Enum):
    CONTAINS = 'contains'
    EXACT = 'exact'


class Where(Enum):
    ANY = "any"
    TITLE = "title"
    DESC = "desc"
    CREATOR = "creator"
    SUBJECT = "subject"
    START_DATE = "start_date"
    END_DATE = "end_date"
    SYSTEM_NUMBER = "system_number"
    SHELFMARK = "shelfmark"
    PUBLISHER = "publisher"
    LANGUAGE = "language"


DATE_FORMAT = ["yyyyMMdd", "yyyy"]
