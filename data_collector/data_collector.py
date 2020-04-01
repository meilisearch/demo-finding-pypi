import requests
import conf

from bs4 import BeautifulSoup
from Package import Package
from meili_index import get_or_create_meilisearch_index

if __name__ == ("__main__"):

    indexed_counter = 0
    pkg_errors = []

    # Create a Meilisearch index
    index = get_or_create_meilisearch_index()
    if index is None:
        exit("ERROR: Couldn't create a Meilisearch index")

    # Get a list of PyPI available packages
    pkg_list_response = requests.get(conf.SIMPLE_API_URL)
    soup = BeautifulSoup(pkg_list_response.text, "html.parser")
    all_pkg = soup.find_all('a')

    # Handle a single package
    for pkg_link in all_pkg:
        pkg = Package(pkg_link.get_text())
        pkg, update_status = pkg.update_pypi_data()
        if update_status is conf.STATUS_ERR:
            pkg_errors.append(pkg.name)
            continue
        try:
            index.add_documents([pkg.__dict__])
            indexed_counter += 1
        except Exception as e:
            print("ERROR INDEXING:", e)
        print("{:7}: {}".format(indexed_counter, pkg))
        if conf.pkg_count_limit is not None:
            if indexed_counter >= conf.pkg_count_limit:
                break

    # Log information to console
    print("Updated package count:", indexed_counter)
    if len(pkg_errors) > 0:
        print("Couldn't find/update following packages:", pkg_errors)
