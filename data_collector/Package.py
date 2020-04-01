import conf
import requests
import json


class Package():

    name = ""
    version = ""
    description = ""
    project_url = ""
    json_data_url = ""
    downloads = 0

    def __init__(self, name):

        self.name = name
        self.json_data_url = "{}{}/json".format(conf.PYPI_API_URL, self.name)

    def __str__(self):

        return "Package: {}, version: {}".format(self.name, self.version)

    def update_object_data(self, json_data):

        self.name = json_data["name"]
        self.version = json_data["version"]
        self.description = json_data["description"]
        self.project_url = json_data["project_url"]

    def update_pypi_data(self):

        req = requests.get(self.json_data_url)
        if req.status_code == 200:
            try:
                json_data = json.loads(req.text)["info"]
                self.update_object_data(json_data)
                return self, conf.STATUS_OK
            except Exception as e:
                print("Error for package {}: {}".format(self.name, e))
                return self, conf.STATUS_ERR
        else:
            print("Error {} in request for package {}. URL: {}".format(
                req.status_code,
                self.name,
                self.json_data_url
            ))
            return self, conf.STATUS_ERR
