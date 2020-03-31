from bs4 import BeautifulSoup
import requests
import json

API_URL = "https://pypi.org/"
package_counter_limit = 100


class Package():

    name = ""
    version = ""
    description = ""
    project_url = ""
    downloads = ""

    def __init__(self, name, version, description, project_url, downloads=0):
        self.name = name
        self.version = version
        self.description = description
        self.project_url = project_url
        self.downloads = downloads

    def __str__(self):
        return "Package: {}, version: {}".format(self.name, self.version)


if __name__ == ("__main__"):

    package_list_response = requests.get(API_URL + "/simple/")
    soup = BeautifulSoup(package_list_response.text, "html.parser")
    package_list = []

    for link in soup.find_all('a'):
        name = link.get_text()
        req = requests.get("https://pypi.org/pypi/" + name + "/json")
        if req.status_code == 200:
            try:
                json_data = json.loads(req.text)["info"]
                package = Package(
                    name = json_data["name"],
                    version = json_data["version"],
                    description = json_data["description"],
                    project_url = json_data["project_url"],
                )
                package_list.append(package)
                print(package)
            except Exception as e:
                print("ERROR ({}): {}".format(name, e))
        if len(package_list) >= package_counter_limit:
            break


    print("Package count:", len(package_list))
