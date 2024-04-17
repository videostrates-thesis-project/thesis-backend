import unittest
from thesis_backend.azure_video_indexer.azure_video_indexer_client import AzureVideoIndexerClient, VideoStatus, \
    ErrorResponse, VideoMetadata, VideoList
from tests.azure_video_indexer.test_case_with_mocked_requests import TestCaseWithMockedRequests


class TestAzureVideoIndexerClient(TestCaseWithMockedRequests, unittest.TestCase):
    def setUp(self):
        self.azure_video_indexer_client = AzureVideoIndexerClient("account_id", "primary_key")

    def test_index_video(self):
        new_video_url = "new-video.mp4"
        video_status = self.azure_video_indexer_client.index_video(new_video_url, 'new-video')
        assert isinstance(video_status, VideoStatus)
        assert isinstance(video_status.url, str)
        assert video_status.url == new_video_url
        assert video_status.state == "Uploaded"
        assert video_status.progress == 1

    def test_index_video_invalid_url(self):
        video_status = self.azure_video_indexer_client.index_video(self.invalid_video_url, "invalid_video")
        assert isinstance(video_status, ErrorResponse)
        assert isinstance(video_status.error_type, str)
        assert isinstance(video_status.message, str)

    def test_get_videos(self):
        videos = self.azure_video_indexer_client.get_videos()
        assert isinstance(videos, VideoList)
        assert len(videos) == 2
        assert videos[self.existing_video_url].id == self.existing_video_id

    def test_get_video_metadata(self):
        video_metadata = self.azure_video_indexer_client.get_video_metadata(self.existing_video_id)
        assert isinstance(video_metadata, VideoMetadata)
        assert video_metadata.id == self.existing_video_id
