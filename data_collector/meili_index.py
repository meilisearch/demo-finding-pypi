import conf
import meilisearch

# TODO: Error handling


def get_or_create_meilisearch_index():

    if (conf.PYPI_MEILI_URL is None or conf.PYPI_MEILI_KEY is None):
        exit("""
            ERROR:
            Set your own key and url as environment variables
            - PYPI_MEILI_URL
            - PYPI_MEILI_KEY.
            See documentation at https://docs.meilisearch.com/
            """)
    client = meilisearch.Client(conf.PYPI_MEILI_URL, conf.PYPI_MEILI_KEY)
    try:
        index = client.create_index(conf.INDEX_UUID, primary_key="name")
        return index
    except Exception as e:
        print("ERROR: Couldn't create index", e)
    try:
        index = client.get_index(conf.INDEX_UUID)
        return index
    except Exception as e:
        print("ERROR: Couldn't get index", e)
    return None
