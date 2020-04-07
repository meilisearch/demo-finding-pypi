# finding-pypi
WIP: Alternative search bar for PyPI packages

[proper README.md coming]

Collect packages info and index to MeiliSearch:

1. git clone https://github.com/meilisearch/finding-pypi.git  
2. cd finding-pypi  
3. python3 -m venv env_finding_pypi  
4. source env_finding_pypi/bin/activate  
5. pip install -r requirements.txt  
6. export PYPI_MEILI_URL="SOME_URL"
7. export PYPI_MEILI_KEY="SOME_KEY"
8. python data_collector/package_collector.py

Collect Downloads data from GCP:

1. Set up your account as described in https://github.com/ofek/pypinfo
2. GOOGLE_APPLICATION_CREDENTIALS=[path_to_creds_json_file...] python data_collector/downloads_collector.py
