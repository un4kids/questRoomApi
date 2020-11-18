import requests
import os


class ApiRequests(object):
    def __init__(self, mac="mac", data={}):
        self.token = os.environ.get("TOKEN")
        self.api_quest_url = os.environ.get("API_QUESTS_URL")
        self.mac = mac
        self.data = data

    def _create_request_header(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def _add_mac_to_url(self, url):
        return url + self.mac + "/"

    def _check_response(self, response):
        if response.status_code == 404:
            return False
        else:
            return True

    def get_all_quests(self):
        headers = self._create_request_header()
        url = self.api_quest_url
        response = requests.get(url, headers=headers)
        return response

    def post_quest(self):
        headers = self._create_request_header()
        url = self.api_quest_url
        response = requests.post(url, headers=headers, json=self.data)
        return response
