import conf
import meilisearch

def get_or_create_meilisearch_index():
    # TODO: Error handling
    if (conf.PYPI_MEILISEARCH_URL is None or conf.PYPI_MEILISEARCH_KEY is None):
        exit("""
            ERROR:
            Set your own key and url as environment variables
            - PYPI_MEILISEARCH_URL
            - PYPI_MEILISEARCH_KEY.
            See documentation at https://docs.meilisearch.com/
            """)
    client = meilisearch.Client(conf.PYPI_MEILISEARCH_URL, conf.PYPI_MEILISEARCH_KEY)
    try :
        index = client.create_index(conf.INDEX_UUID)
        return index
    except Exception as e:
        # Couldn't create index
        print("ERROR: Couldn't create index", e)
        pass
    try :
        index = client.get_index(conf.INDEX_UUID)
        return index
    except Exception as e:
        # Couldn't get index
        print("ERROR: Couldn't get index", e)
        pass
    return None
