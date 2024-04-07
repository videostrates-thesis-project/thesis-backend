from __future__ import annotations

from typing import NamedTuple, Mapping, Sequence

import requests

from src.thesis_backend.azure_video_indexer.metadata import MetadataStore, MetadataSegment, MetadataCollection, \
    SearchQuery, SearchResult
from src.thesis_backend.utils.string_to_time import string_to_time
from src.thesis_backend.utils.throttle import throttle

LOCATION = "trial"
TOKEN_EXPIRATION = 59 * 60  # 59 minutes
VIDEO_LIST_REFRESH = 1  # 1 second


class AzureVideoIndexerToken:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id: str = account_id
        self.__headers: dict[str, str] = {"Ocp-Apim-Subscription-Key": primary_key}

    @property
    @throttle(interval=TOKEN_EXPIRATION)
    def token(self) -> str:
        url = f"https://api.videoindexer.ai/auth/{LOCATION}/Accounts/{self.__account_id}/AccessToken"
        query_params = {"allowEdit": "true"}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return response.json()


class VideoStatus(NamedTuple):
    id: str
    url: str
    state: str
    progress: int


class AzureVideoCatalog:
    def __init__(self, account_id: str, primary_key: str, access_token: AzureVideoIndexerToken) -> None:
        self.__account_id = account_id
        self.__access_token = access_token
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}
        self.__videos: Mapping[str, VideoStatus] = {}
        self.__metadata: MetadataStore = MetadataStore()

    @throttle(interval=VIDEO_LIST_REFRESH)
    def __refresh_metadata(self) -> None:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos"
        query_params = {"accessToken": self.__access_token.token}
        response = requests.get(url, params=query_params, headers=self.__headers)
        videos_response = response.json()["results"]
        videos = {}
        for video in videos_response:
            video_id = video["id"]
            video_url = video["description"]
            video_state = video["state"]
            # Remove '%' from the end of the string and convert to int
            video_progress = int(video["processingProgress"][:-1])
            if video_url:
                videos[video_url] = (VideoStatus(video_id, video_url, video_state, video_progress))
                if video_state == "Processed" and not self.__metadata.get_video(video_url):
                    self.__metadata.add_video(video_url, self.__get_video_metadata(video_id))
        self.__videos: Mapping[str, VideoStatus] = videos
        return

    def __get_video_metadata(self, video_id: str) -> MetadataCollection:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos/{video_id}/Index"
        query_params = {"accessToken": self.__access_token.token}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return video_index_to_metadata(response.json())

    @property
    def videos(self) -> Mapping[str, VideoStatus]:
        self.__refresh_metadata()
        return self.__videos

    def search(self, query: SearchQuery) -> Sequence[SearchResult]:
        self.__refresh_metadata()
        return self.__metadata.search(query)


class AzureVideoIndexer:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id = account_id
        self.__access_token = AzureVideoIndexerToken(account_id, primary_key)
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
        return VideoStatus(response["id"], video_url, response["state"], response["processingProgress"])

    def get_videos_status(self, urls: list[str]) -> Mapping[str, VideoStatus]:
        filtered_videos = {k: v for k, v in self.__video_catalog.videos.items() if k in urls}
        return filtered_videos

    def search(self, query: SearchQuery) -> Sequence[SearchResult]:
        return self.__video_catalog.search(query)


def video_index_to_metadata(video_index: dict) -> MetadataCollection:
    metadata: list[MetadataSegment] = []
    transcript = video_index["videos"][0]["insights"].get("transcript", [])
    for segment in transcript:
        for instance in segment["instances"]:
            start = string_to_time(instance["start"])
            end = string_to_time(instance["end"])
            metadata.append(MetadataSegment(start, end, segment["text"], segment["confidence"]))
    return MetadataCollection(metadata)
