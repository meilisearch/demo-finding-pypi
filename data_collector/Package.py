import conf
import requests
import json
import hashlib


class Package():

    _id = ""
    name = ""
    version = ""
    description = ""
    project_url = ""
    json_data_url = ""
    downloads = 0

    def __init__(self, name):
        self.name = name
        md5t = hashlib.md5()
        md5t.update(name.encode('utf-8'))
        self._id = md5t.hexdigest()
        self.json_data_url = "{}{}/json".format(conf.PYPI_API_URL, self.name)

    def __str__(self):

        return "Package: {}, version: {}".format(self.name, self.version)

    def update_object_data(self, json_data):

        self.name = json_data["name"]
        self.version = json_data["version"]
        self.description = json_data["summary"]
        self.project_url = json_data["project_url"]

    async def update_pypi_data(self):

        req = requests.get(self.json_data_url)
        if req.status_code == 200:
            try:
                json_data = json.loads(req.text)["info"]
                self.update_object_data(json_data)
            except Exception as e:
                print("Error for package {}: {}".format(self.name, e))
        else:
            print("Error {} in request for package {}. URL: {}".format(
                req.status_code,
                self.name,
                self.json_data_url
            ))
