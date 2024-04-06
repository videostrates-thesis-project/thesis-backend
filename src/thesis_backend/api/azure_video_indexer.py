import time

import requests

LOCATION = "trial"
TOKEN_EXPIRATION = 59 * 60  # 59 minutes


class VideoIndexerToken:
    def __init__(self, account_id, primary_key):
        self.__account_id = account_id
        self.__access_token = None
        self.__access_token_expires = -1
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}

    @property
    def token(self):
        current_time = time.time()
        if self.__access_token is None or self.__access_token_expires < current_time:
            token = self.__get_access_token()
            self.__access_token = token
            self.__access_token_expires = current_time + TOKEN_EXPIRATION
        return self.__access_token

    def __get_access_token(self):
        url = f"https://api.videoindexer.ai/auth/{LOCATION}/Accounts/{self.__account_id}/AccessToken"
        query_params = {"allowEdit": "true"}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return response.json()


class AzureVideoIndexer:
    def __init__(self, account_id, primary_key):
        self.account_id = account_id
        self.__access_token = VideoIndexerToken(account_id, primary_key)
        self.headers = {"Ocp-Apim-Subscription-Key": primary_key}

    def upload_video(self, video_url, video_name):
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.account_id}/Videos"
        query_params = {
            "accessToken": self.__access_token.token,
            "videoUrl": video_url,
            "name": video_name
        }
        response = requests.post(url, params=query_params, headers=self.headers)
        return response.json()

    def get_video_index(self, video_id):
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.account_id}/Videos/{video_id}/Index"
        query_params = {"accessToken": self.__access_token.token}
        response = requests.get(url, params=query_params, headers=self.headers)
        return response.json()
    #
    # def get_video_index_by_id(self, video_id):
    #     url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.account_id}/Videos/{video_id}/Index?accessToken={self.access_token}"
    #     response = requests.get(url, headers=self.headers)
    #     return response.json()
