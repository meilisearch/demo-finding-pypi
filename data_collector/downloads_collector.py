from google.cloud import bigquery
import os
import json
from datetime import datetime, timedelta


client = bigquery.Client()
d = datetime.now().replace(day=1) - timedelta(days=1)
table_prefix_last_month = d.strftime("%Y%m")
current_offset=0

QUERY = (
    "SELECT file.project AS name, COUNT(*) AS download_count, \
    FROM `the-psf.pypi.downloads{date_prefix}*` \
    GROUP BY name \
    ORDER BY download_count DESC \
    LIMIT {limit} \
    OFFSET {offset}".format(
        date_prefix=table_prefix_last_month,
        limit=100,
        offset=0,
    )
)
query_job = client.query(QUERY)
rows = query_job.result()

for row in rows:
    print(row.name, row.download_count)
