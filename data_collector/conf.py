import os

# Set pkg_count_limit to None for no limit
pkg_count_limit = None

# Set the size of the batch that will be treated by MeiliSearch
pkg_indexing_batch_size = 500

# Set the offset to start treateing package list at a given index
pkg_list_offset = 220000

# MeiliSearch params
INDEX_UUID = "TEST_ASYNCIO"
PYPI_MEILI_URL = os.getenv('PYPI_MEILI_URL')
PYPI_MEILI_KEY = os.getenv('PYPI_MEILI_KEY')

# Data sources
SIMPLE_API_URL = "https://pypi.org/simple/"
PYPI_API_URL = "https://pypi.org/pypi/"

# Misc
STATUS_OK = 0
STATUS_ERR = 1
