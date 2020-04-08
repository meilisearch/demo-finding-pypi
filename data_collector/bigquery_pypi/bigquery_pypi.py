import os
import pickle
from datetime import datetime, timedelta
from google.cloud import bigquery

date = datetime.now().replace(day=1) - timedelta(days=1)
table_prefix_date = date.strftime("%Y%m")
downloads_file = "data_collector/bigquery_pypi/data/downloads_{}.pkl".format(table_prefix_date)


def get_most_downloaded_pkgs(limit=200000, offset=None):

    downloads_dict = {}
    client = bigquery.Client()

    sql_request = "SELECT file.project AS name, COUNT(*) AS download_count, \
    FROM `the-psf.pypi.downloads{}*` \
    GROUP BY name \
    HAVING download_count>50 \
    ORDER BY download_count DESC".format(table_prefix_date)
    if limit is not None:
        sql_request += " LIMIT {}".format(limit)
    if offset is not None:
        sql_request += " OFFSET {}".format(offset)
    query_job = client.query(sql_request)
    rows = query_job.result()

    for row in rows:
        downloads_dict[row.name] = row.download_count
    return downloads_dict


def downloads_dict_from_file():

    if os.path.isfile(downloads_file):
        f = open(downloads_file)
        print("Downloads file found: {}".format(downloads_file))
    else:
        print("Downloads file NOT found. Requesting downloads from Bigquery")
        downloads_dict = get_most_downloaded_pkgs()
        try:
            with open(downloads_file, 'wb') as f:
                pickle.dump(downloads_dict, f, pickle.HIGHEST_PROTOCOL)
                print("Downloads file created: {}".format(downloads_file))
        except IOError as e:
            print("I/O ERROR: {}".format(e))
    with open(downloads_file, 'rb') as f:
        dict = pickle.load(f)
        print("Found downloads data for {} packages".format(len(dict)))
        return dict


if __name__ == "__main__":

    dict = get_or_create_downloads_dict_from_file()
