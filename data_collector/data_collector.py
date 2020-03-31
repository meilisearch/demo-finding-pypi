import requests
from bs4 import BeautifulSoup
import conf
from Package import Package, handle_single_package
from meili_indexer import get_or_create_meilisearch_index

if __name__ == ("__main__"):

    package_list = []
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
        pkg_name = pkg_link.get_text()
        handle_single_package(pkg_name, package_list, pkg_errors)
        if conf.pkg_count_limit is not None and len(package_list) >= conf.pkg_count_limit:
            break

    # Log information to console
    print("Package count:", len(package_list))
    if len(pkg_errors) > 0 :
        print("Couldn't find following packages:", pkg_errors)
