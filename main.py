import os
import requests

HTTP_STATUS_CREATE: int = 201
TOKEN = ""

class YaUploader:
    URL_UPLOAD_LINK: str = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, token: str):
        self.token = token

    @property
    def header(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def _get_upload_link(self, ya_disk_path: str):
        params = {"path": ya_disk_path, "overwrite": "true"}
        response = requests.get(self.URL_UPLOAD_LINK, headers=self.header, params=params)
        upload_url = response.json().get("href")

        return upload_url

    def upload_file(self, file_path: str):
        if os.path.isfile(file_path):
            ya_disk_path = file_path[file_path.rfind("\\") + 1:]
            upload_link = self._get_upload_link(ya_disk_path)
            with open(file_path, 'rb') as file_obj:
                response = requests.put(upload_link, data=file_obj)
                if response.status_code == HTTP_STATUS_CREATE:
                    print(f"Downloaded successfully, response code is {response.status_code}")
        else:
            dir_list = os.listdir(file_path)
            for new_dir in dir_list:
                self.upload_file(os.path.join(file_path, new_dir))


def get_most_intelligence_hero(url: str, hero_list):
    hero_dict = (requests.get(url)).json()
    max_int = -1
    int_hero = ""
    for hero in hero_dict:
        if hero.get("name") in hero_list:
            if hero["powerstats"]["intelligence"] > max_int:
                max_int = hero["powerstats"]["intelligence"]
                int_hero = hero["name"]
    return int_hero


if __name__ == '__main__':
    URL_HERO_API: str = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
    list = ["Hulk", "Captain America", "Thanos"]
    print(get_most_intelligence_hero(URL_HERO_API, list))

    instance = YaUploader(TOKEN)
    instance.upload_file(os.path.join(os.getcwd(), "to_upload"))
