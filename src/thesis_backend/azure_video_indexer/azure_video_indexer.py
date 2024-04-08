from __future__ import annotations
from typing import Mapping, Sequence
from src.thesis_backend.azure_video_indexer.azure_video_indexer_client import AzureVideoIndexerClient, VideoStatus, \
    ErrorResponse
from src.thesis_backend.azure_video_indexer.metadata import MetadataStore, SearchResult, SearchedVideo, \
    MetadataCollection, MetadataSegment
from src.thesis_backend.utils.throttle import throttle

VIDEO_LIST_REFRESH_RATE = 10  # 10 seconds


class AzureVideoCatalog:
    def __init__(self, video_indexer_client: AzureVideoIndexerClient) -> None:
        self.__video_indexer_client = video_indexer_client
        self.__videos: Mapping[str, VideoStatus] = {}
        self.__metadata: MetadataStore = MetadataStore()

    @throttle(interval=VIDEO_LIST_REFRESH_RATE)
    def __refresh_metadata(self) -> None:
        refreshed_videos = self.__video_indexer_client.get_videos()
        raise_if_error(refreshed_videos)
        for url, video in refreshed_videos.items():
            if video.state == "Processed" and not self.__metadata.get_video(url):
                response = self.__video_indexer_client.get_video_metadata(video.id)
                raise_if_error(response)
                metadata = MetadataCollection([MetadataSegment(*t) for t in response.transcript])
                self.__metadata.add_video(url, metadata)
        self.__videos: Mapping[str, VideoStatus] = refreshed_videos

    @property
    def videos(self) -> Mapping[str, VideoStatus]:
        self.__refresh_metadata()
        return self.__videos

    def add_video(self, video_status: VideoStatus) -> None:
        self.__videos = self.__videos | {video_status.url: video_status}

    def search(self, query: str, videos: list[SearchedVideo]) -> Sequence[SearchResult]:
        self.__refresh_metadata()
        return self.__metadata.search(query, videos)


class AzureVideoIndexer:
    def __init__(self, account_id: str, primary_key: str) -> None:
        self.__video_indexer_client = AzureVideoIndexerClient(account_id, primary_key)
        self.__video_catalog = AzureVideoCatalog(self.__video_indexer_client)

    def upload_video(self, video_url: str, video_name: str) -> VideoStatus:
        video_status = self.__video_indexer_client.index_video(video_url, video_name)
        raise_if_error(video_status)
        self.__video_catalog.add_video(video_status)
        return video_status

    def get_videos_status(self, urls: list[str]) -> Mapping[str, VideoStatus]:
        filtered_videos = {k: v for k, v in self.__video_catalog.videos.items() if k in urls}
        return filtered_videos

    def search(self, query: str, videos: list[SearchedVideo]) -> Sequence[SearchResult]:
        return self.__video_catalog.search(query, videos)


def raise_if_error(response: any) -> None:
    if isinstance(response, ErrorResponse):
        raise Exception(f"{response.error_type}: {response.message}")
