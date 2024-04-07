import os
import unittest

from dotenv import load_dotenv

from src.thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoIndexer, AzureVideoIndexerToken, \
    AzureVideoCatalog
from src.thesis_backend.azure_video_indexer.metadata import SearchedVideo

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


class TestAzureVideoIndexer(unittest.TestCase):
    def setUp(self):
        self.account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
        self.primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")
        self.video_big_buck_bunny = "https://storage.googleapis.com/videostrates.appspot.com/files/f90454fd-1616-4845-8252-f2978bab22a7.mp4"
        self.video_sprite_fright = "https://storage.googleapis.com/videostrates.appspot.com/files/1f4c33d5-b98b-45ea-81e2-1e10ef14ace7.mp4"
        self.video_name = "test_video"
        self.video_id = "84505873fd"

    def test_get_access_token(self):
        azure_token = AzureVideoIndexerToken(self.account_id, self.primary_key)
        token = azure_token.token
        print(token)
        assert token is not None
        assert isinstance(token, str)

    def test_video_catalog(self):
        azure_token = AzureVideoIndexerToken(self.account_id, self.primary_key)
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
        videos = azure_video_indexer.get_videos_status([self.video_big_buck_bunny])
        assert videos is not None
        assert len(videos) is 1
        assert videos[self.video_big_buck_bunny].url == self.video_big_buck_bunny
        assert videos[self.video_big_buck_bunny].state == "Processed"
        assert videos[self.video_big_buck_bunny].progress == 100

    def test_get_video_status_invalid_url(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        videos = azure_video_indexer.get_videos_status(["invalid"])
        assert videos is not None
        assert len(videos) is 0

    def test_upload_video(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        video_status = azure_video_indexer.upload_video(self.video_big_buck_bunny, self.video_name)
        assert video_status is not None
        assert isinstance(video_status, tuple)
        assert video_status.url == self.video_big_buck_bunny
        assert isinstance(video_status.state, str)

    def test_upload_video_invalid_url(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        # Should raise an exception
        with self.assertRaises(Exception):
            azure_video_indexer.upload_video("invalid", self.video_name)

    def test_search_videos(self):
        azure_video_indexer = AzureVideoIndexer(self.account_id, self.primary_key)
        query = "fun guys"
        videos = [SearchedVideo(self.video_sprite_fright, 0, 60)]
        results = azure_video_indexer.search(query, videos)
        print(results)
        assert results is not None
        assert len(results) > 0
        for result in results:
            assert result.url == self.video_sprite_fright
            assert isinstance(result.match.content, str)
            assert isinstance(result.match.start, float)
            assert isinstance(result.match.end, float)
            assert isinstance(result.confidence, float)
            assert 0 <= result.confidence <= 1
