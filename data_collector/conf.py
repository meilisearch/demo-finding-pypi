import os

# Set pkg_count_limit to None for no limit
pkg_cnt_limit = None

# Set the size of the batch that will be treated by MeiliSearch
pkg_indexing_batch_size = 1000

# Set the scheduler number of concurrent tasks
scheduler_max_tasks = 100

# Set the offset to start treating the package list
pkg_list_offset = 0

# MeiliSearch params
INDEX_UUID = "PYPIPKG"
PYPI_MEILI_URL = os.getenv('PYPI_MEILI_URL')
PYPI_MEILI_KEY = os.getenv('PYPI_MEILI_KEY')

# Data sources
SIMPLE_API_URL = "https://pypi.org/simple/"
PYPI_API_URL = "https://pypi.org/pypi/"

SHOW_PYPI_HTTP_ERRORS = False
