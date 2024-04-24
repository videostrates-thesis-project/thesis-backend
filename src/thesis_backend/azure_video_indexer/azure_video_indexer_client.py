from __future__ import annotations
import requests
from collections import UserDict
from typing import Mapping, NamedTuple
from thesis_backend.utils.throttle import throttle
from thesis_backend.utils.time_str_to_seconds import time_str_to_seconds

LOCATION = "trial"
TOKEN_EXPIRATION = 59 * 60  # 59 minutes


class VideoStatus(NamedTuple):
    id: str
    url: str
    state: str
    progress: int

    @staticmethod
    def from_response(data: Mapping[str, str]) -> 'VideoStatus':
        return VideoStatus(
            id=data["id"],
            # Use the description field to store the video URL, which can be used as an identifier
            url=data["description"],
            state=data["state"],
            progress=VideoStatus.__parse_percentage_string(data["processingProgress"])
        )

    @staticmethod
    def __parse_percentage_string(string: str) -> int:
        return int(string[:-1])


class TranscriptSegment(NamedTuple):
    start: float
    end: float
    text: str
    confidence: float


class VideoList(UserDict[str, VideoStatus]):
    @staticmethod
    def from_response(data: Mapping[str, any]) -> 'VideoList':
        videos_response = data["results"]
        videos = {}
        for video in videos_response:
            video_url = video["description"]
            if video_url:
                videos[video_url] = VideoStatus.from_response(video)
        return VideoList(videos)


class VideoMetadata(NamedTuple):
    id: str
    url: str
    transcript: list[TranscriptSegment]

    @staticmethod
    def from_response(data: Mapping[str, any]) -> 'VideoMetadata':
        transcript_raw = data["videos"][0]["insights"].get("transcript", [])
        transcript = []
        for segment in transcript_raw:
            for instance in segment["instances"]:
                start = time_str_to_seconds(instance["start"])
                end = time_str_to_seconds(instance["end"])
                transcript.append(TranscriptSegment(start, end, segment["text"], segment["confidence"]))
        return VideoMetadata(id=data["id"], url=data["description"], transcript=transcript)


class ErrorResponse(NamedTuple):
    error_type: str
    message: str

    @staticmethod
    def from_response(data: Mapping[str, str]) -> 'ErrorResponse':
        return ErrorResponse(data["ErrorType"], data["Message"])


class AzureVideoIndexerClient:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__account_id = account_id
        self.__headers = {"Ocp-Apim-Subscription-Key": primary_key}

    @property
    @throttle(interval=TOKEN_EXPIRATION)
    def __access_token(self) -> str:
        url = f"https://api.videoindexer.ai/auth/{LOCATION}/Accounts/{self.__account_id}/AccessToken"
        query_params = {"allowEdit": "true"}
        response = requests.get(url, params=query_params, headers=self.__headers)
        return response.json()

    def index_video(self, video_url: str, video_name: str) -> VideoStatus | ErrorResponse:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos"
        query_params = {
            "accessToken": self.__access_token,
            "videoUrl": video_url,
            "name": video_name,
            "description": video_url
        }
        response = requests.post(url, params=query_params, headers=self.__headers).json()
        if response.get("ErrorType"):
            print("ERROR in index_video")
            print(response)
            return ErrorResponse.from_response(response)

        return VideoStatus.from_response(response)

    def get_videos(self) -> VideoList | ErrorResponse:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos"
        query_params = {"accessToken": self.__access_token}
        response = requests.get(url, params=query_params, headers=self.__headers).json()
        if response.get("ErrorType"):
            print("ERROR in get_videos")
            print(response)
            return ErrorResponse.from_response(response)
        return VideoList.from_response(response)

    def get_video_metadata(self, video_id: str) -> VideoMetadata | ErrorResponse:
        url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{self.__account_id}/Videos/{video_id}/Index"
        query_params = {"accessToken": self.__access_token}
        response = requests.get(url, params=query_params, headers=self.__headers).json()
        if response.get("ErrorType"):
            print("ERROR in get_video_metadata")
            print(response)
            return ErrorResponse.from_response(response)
        return VideoMetadata.from_response(response)
