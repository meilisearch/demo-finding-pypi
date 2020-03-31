import os

# Set pkg_count_limit to None for no limit
pkg_count_limit = None
SIMPLE_API_URL = "https://pypi.org/simple/"
PYPI_API_URL = "https://pypi.org/pypi/"
INDEX_UUID = "PYPIPKG"
PYPI_MEILISEARCH_URL = os.getenv('PYPI_MEILISEARCH_URL')
PYPI_MEILISEARCH_KEY = os.getenv('PYPI_MEILISEARCH_KEY')
