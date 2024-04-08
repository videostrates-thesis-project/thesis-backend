import unittest
from src.thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoIndexer
from src.thesis_backend.azure_video_indexer.metadata import SearchedVideo
from tests.azure_video_indexer.test_case_with_mocked_requests import TestCaseWithMockedRequests


class TestAzureVideoIndexer(TestCaseWithMockedRequests, unittest.TestCase):
    def setUp(self):
        self.azure_video_indexer = AzureVideoIndexer("account_id", "primary_key")

    def test_get_video_status(self):
        print("self.existing_video_url")
        # Clear the cache of @throttle decorator, because the cache is shared between tests.
        self.azure_video_indexer._AzureVideoIndexer__video_catalog._AzureVideoCatalog__refresh_metadata.cache_reset()
        videos = self.azure_video_indexer.get_videos_status([self.existing_video_url])
        print("videos")
        print(videos)
        assert videos is not None
        assert len(videos) is 1
        video = videos[self.existing_video_url]
        assert video.url == self.existing_video_url
        assert video.state == "Processed"
        assert video.progress == 100

    def test_get_video_status_invalid_url(self):
        videos = self.azure_video_indexer.get_videos_status([self.invalid_video_url])
        assert videos is not None
        assert len(videos) is 0

    def test_upload_video(self):
        new_video_url = "new-video.mp4"
        video_status = self.azure_video_indexer.upload_video(new_video_url, "new-video")
        assert video_status is not None
        assert isinstance(video_status, tuple)
        assert video_status.url == new_video_url
        assert isinstance(video_status.state, str)

    def test_search_videos(self):
        query = "cute little"
        videos = [SearchedVideo(self.existing_video_url, 0, 60)]
        results = self.azure_video_indexer.search(query, videos)
        print(results)
        assert results is not None
        assert len(results) > 0
        for result in results:
            assert result.url == self.existing_video_url
            assert isinstance(result.match.content, str)
            assert isinstance(result.match.start, float)
            assert isinstance(result.match.end, float)
            assert isinstance(result.confidence, float)
            assert 0 <= result.confidence <= 1
