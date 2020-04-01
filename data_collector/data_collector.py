import requests
from bs4 import BeautifulSoup
import conf
from Package import Package
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
        pkg = Package(pkg_link.get_text())
        pkg, update_status = pkg.update_pypi_data()
        if update_status is conf.STATUS_ERR:
            pkg_errors.append(pkg.name)
            continue
        package_list.append(pkg)
        counter = len(package_list) - 1
        print("{:7}: {}".format(counter, package_list[counter]))
        if conf.pkg_count_limit is not None and len(package_list) >= conf.pkg_count_limit:
            break

    # Log information to console
    print("Updated package count:", len(package_list))
    if len(pkg_errors) > 0 :
        print("Couldn't find/update following packages:", pkg_errors)
