import os
import json
import csv
from datetime import datetime, timedelta
from google.cloud import bigquery

def get_most_downloaded_pkgs(limit=None, offset=None):
    downloads_dict = {}
    client = bigquery.Client()
    date = datetime.now().replace(day=1) - timedelta(days=1)
    table_prefix_date = date.strftime("%Y%m")
    current_offset=0

    sql_request = "SELECT file.project AS name, COUNT(*) AS download_count, \
    FROM `the-psf.pypi.downloads{}*` \
    GROUP BY name \
    HAVING download_count>1000 \
    ORDER BY download_count DESC".format(table_prefix_date)
    if limit is not None:
        sql_request += "LIMIT {}".format(limit)
    if offset is not None:
        sql_request += "OFFSET {}".format(offset)
    query_job = client.query(sql_request)
    rows = query_job.result()

    for row in rows:
        downloads_dict[row.name] = row.download_count
    return downloads_dict

def update_or_create_downloads_csv_file():
    downloads_dict = get_most_downloaded_pkgs()
    fieldnames=["name", "download_count"]
    try:
        with open("most_downloaded.csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pkg in downloads_dict:
                writer.writerow(pkg)
    except IOError as e:
        print("I/O ERROR: {}".format(e))

if __name__ == "__main__":
    update_or_create_downloads_csv_file()
