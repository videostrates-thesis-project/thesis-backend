import unittest
from typing import Mapping

from thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoCatalog
from thesis_backend.azure_video_indexer.azure_video_indexer_client import AzureVideoIndexerClient, VideoStatus
from tests.azure_video_indexer.test_case_with_mocked_requests import TestCaseWithMockedRequests


class TestAzureVideoCatalog(TestCaseWithMockedRequests, unittest.TestCase):
    def setUp(self):
        video_indexer_client = AzureVideoIndexerClient("account_id", "primary_key")
        self.video_catalog = AzureVideoCatalog(video_indexer_client)

    def test_videos(self):
        videos = self.video_catalog.videos
        assert videos is not None
        assert isinstance(videos, Mapping)
        assert len(videos) > 0
        assert self.existing_video_url in videos
        for url, video in videos.items():
            assert video.url is not None
            assert url == video.url
            assert video.state is not None
            assert video.progress is not None
            assert isinstance(video.url, str)
            assert isinstance(video.state, str)
            assert isinstance(video.progress, int)
            assert 0 <= video.progress <= 100

    def test_add_video(self):
        # Trigger fetch of videos. Refreshing of the videos is throttled, so the next call won't fetch the videos again.
        _ = self.video_catalog.videos
        new_video_url = "new-video.mp4"
        new_video_state = "Processed"
        video = VideoStatus("new-id", new_video_url, new_video_state, 1)
        self.video_catalog.add_video(video)
        videos = self.video_catalog.videos
        assert new_video_url in videos
        video_status = videos[new_video_url]
        assert isinstance(video_status, tuple)
        assert video_status.url == new_video_url
        assert video_status.state == new_video_state
