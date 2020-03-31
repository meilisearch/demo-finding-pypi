import conf
import requests
import json

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

def create_pkg_object(package_list, json_data):

    package_list.append(
        Package(
            name = json_data["name"],
            version = json_data["version"],
            description = json_data["description"],
            project_url = json_data["project_url"],
        )
    )
    counter = len(package_list) - 1
    print("{:7}: {}".format(counter, package_list[counter]))

def handle_single_package(pkg_name, package_list, pkg_errors):
    json_url = "{}{}/json".format(conf.PYPI_API_URL, pkg_name)
    req = requests.get(json_url)
    if req.status_code == 200:
        try:
            json_data = json.loads(req.text)["info"]
            create_pkg_object(package_list, json_data)
        except Exception as e:
            print("Error for package {}: {}".format(pkg_name, e))
            pkg_errors.append(pkg_name)
    else:
        print("Error {} in request for package {}. URL: {}".format(
            req.status_code,
            pkg_name,
            json_url
        ))
        pkg_errors.append(pkg_name)
