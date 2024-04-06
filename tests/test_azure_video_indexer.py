import os
import unittest

from dotenv import load_dotenv

from src.thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoIndexer, VideoIndexerToken, \
    AzureVideoCatalog

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


class TestAzureVideoIndexer(unittest.TestCase):
    def setUp(self):
        self.account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
        self.primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")
        self.video_url = "https://storage.googleapis.com/videostrates.appspot.com/files/f90454fd-1616-4845-8252-f2978bab22a7.mp4"
        self.video_name = "test_video"
        self.video_id = "84505873fd"

    def test_get_access_token(self):
        azure_token = VideoIndexerToken(self.account_id, self.primary_key)
        token = azure_token.token
        assert token is not None
        assert isinstance(token, str)

    def test_video_catalog(self):
        azure_token = VideoIndexerToken(self.account_id, self.primary_key)
        video_catalog = AzureVideoCatalog(self.account_id, self.primary_key, azure_token)
        videos = video_catalog.videos
        assert videos is not None
        assert isinstance(videos, dict)
        assert len(videos) > 0
        for url, video in videos.items():
            assert video.url is not None
            assert url == video.url
            assert video.state is not None
            assert video.progress is not None
            assert isinstance(video.url, str)
            assert isinstance(video.state, str)
            assert isinstance(video.progress, int)
            assert 0 <= video.progress <= 100

    def test_get_video_status(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        videos = azure_video_indexer.get_videos_status([self.video_url])
        assert videos is not None
        assert len(videos) is 1
        assert videos[self.video_url].url == self.video_url
        assert videos[self.video_url].state == "Processed"
        assert videos[self.video_url].progress == 100

    def test_upload_video(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        video_status = azure_video_indexer.upload_video(self.video_url, self.video_name)
        assert video_status is not None
        assert isinstance(video_status, tuple)
        assert video_status.url == self.video_url
        assert isinstance(video_status.state, str)

    def test_get_video_index(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        response = azure_video_indexer.get_video_index(self.video_id)
        assert response is not None
        assert isinstance(response, dict)
        assert "id" in response
        assert response["id"] == self.video_id
