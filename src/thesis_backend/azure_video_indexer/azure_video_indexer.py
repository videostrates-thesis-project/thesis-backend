import time
from typing import NamedTuple, Mapping

import requests

LOCATION = "trial"
TOKEN_EXPIRATION = 59 * 60  # 59 minutes
VIDEO_LIST_REFRESH = 1  # 1 second


class VideoIndexerToken:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id = account_id
        self.__access_token = None
        self.__access_token_expires = -1
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}

    @property
    def token(self) -> str:
        current_time = time.time()
        if self.__access_token is None or self.__access_token_expires < current_time:
            token = self.__get_access_token()
            self.__access_token = token
            self.__access_token_expires = current_time + TOKEN_EXPIRATION
        return self.__access_token

    def __get_access_token(self) -> str:
        url = f"https://api.videoindexer.ai/auth/{LOCATION}/Accounts/{self.__account_id}/AccessToken"
        query_params = {"allowEdit": "true"}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return response.json()


class VideoStatus(NamedTuple):
    url: str
    state: str
    progress: int


class AzureVideoCatalog:
    def __init__(self, account_id: str, primary_key: str, access_token: VideoIndexerToken) -> None:
        self.__account_id = account_id
        self.__access_token = access_token
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}
        self.__videos: Mapping[str, VideoStatus] = {}
        self.__next_refresh = -1

    def __refresh_videos(self) -> None:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos"
        query_params = {"accessToken": self.__access_token.token}
        response = requests.get(url, params=query_params, headers=self.__headers)
        videos = response.json()["results"]
        self.__videos = {}
        for video in videos:
            video_url = video["description"]
            video_state = video["state"]
            # Remove '%' from the end of the string and convert to int
            video_progress = int(video["processingProgress"][:-1])
            if video_url:
                self.__videos[video_url] = (VideoStatus(video_url, video_state, video_progress))
        return

    @property
    def videos(self) -> Mapping[str, VideoStatus]:
        current_time = time.time()
        if self.__next_refresh < current_time:
            self.__next_refresh = current_time + VIDEO_LIST_REFRESH
            self.__refresh_videos()
        return self.__videos


class AzureVideoIndexer:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id = account_id
        self.__access_token = VideoIndexerToken(account_id, primary_key)
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}
        self.__video_catalog = AzureVideoCatalog(account_id, primary_key, self.__access_token)

    def upload_video(self, video_url: str, video_name: str) -> VideoStatus:
        if video_url in self.__video_catalog.videos:
            return self.__video_catalog.videos[video_url]
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos"
        query_params = {
            "accessToken": self.__access_token.token,
            "videoUrl": video_url,
            "name": video_name,
            "description": video_url
        }
        response = requests.post(url, params=query_params, headers=self.__headers).json()
        return VideoStatus(video_url, response["state"], response["processingProgress"])

    def get_video_index(self, video_id: str) -> dict:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos/{video_id}/Index"
        query_params = {"accessToken": self.__access_token.token}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return response.json()

    def get_videos_status(self, urls: list[str]) -> Mapping[str, VideoStatus]:
        filtered_videos = {k: v for k, v in self.__video_catalog.videos.items() if k in urls}
        return filtered_videos
