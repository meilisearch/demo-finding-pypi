import os

# Set pkg_count_limit to None for no limit
pkg_count_limit = None
pkg_indexing_batch_size = 100

# MeiliSearch params
INDEX_UUID = "TESTMD5"
PYPI_MEILI_URL = os.getenv('PYPI_MEILI_URL')
PYPI_MEILI_KEY = os.getenv('PYPI_MEILI_KEY')

# Data sources
SIMPLE_API_URL = "https://pypi.org/simple/"
PYPI_API_URL = "https://pypi.org/pypi/"

# Misc
STATUS_OK = 0
STATUS_ERR = 1
