=====
Usage
=====

To use National Library of Israel API in a project::

    import nli_api
    from nli_api.query import Query

    api = nli_api.get_nli_api("API_KEY")

    api.search("hello")
    api.search("ראש ממשלה", page=2)

    q = Query("מלחמה", exact=True) & Query("כיפור", exact=True)
    res = api.search(q, all_pages=True)

