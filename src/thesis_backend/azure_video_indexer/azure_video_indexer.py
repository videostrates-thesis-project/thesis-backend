from __future__ import annotations

import time
from typing import NamedTuple, Mapping

import requests

LOCATION = "trial"
TOKEN_EXPIRATION = 59 * 60  # 59 minutes
VIDEO_LIST_REFRESH = 1  # 1 second


def with_auto_refresh(refresh_func: callable, refresh_interval: int) -> callable:
    """
    Decorator performing automatic refresh of the decorated function.
    Intended to be used for properties that require periodic refresh, such as access tokens.
    """

    def inner(func: callable) -> callable:
        def wrapper(self, *args, **kwargs):
            next_refresh_time = self.__dict__.get("__next_refresh_time")
            if not next_refresh_time or time.time() > next_refresh_time:
                refresh_func(self)
                self.__dict__["__next_refresh_time"] = time.time() + refresh_interval
            return func(self, *args, **kwargs)

        return wrapper

    return inner


class VideoIndexerToken:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id: str = account_id
        self.__access_token: str = ""
        self.__headers: dict[str, str] = {"Ocp-Apim-Subscription-Key": primary_key}

    def __refresh_access_token(self) -> None:
        url = f"https://api.videoindexer.ai/auth/{LOCATION}/Accounts/{self.__account_id}/AccessToken"
        query_params = {"allowEdit": "true"}
        response = requests.get(url, params=query_params, headers=self.__headers)
        self.__access_token = response.json()

    @property
    @with_auto_refresh(refresh_func=__refresh_access_token, refresh_interval=TOKEN_EXPIRATION)
    def token(self) -> str:
        return self.__access_token


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
    @with_auto_refresh(refresh_func=__refresh_videos, refresh_interval=VIDEO_LIST_REFRESH)
    def videos(self) -> Mapping[str, VideoStatus]:
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
