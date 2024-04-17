import os
import unittest
from dotenv import load_dotenv
from src.thesis_backend.azure_video_indexer.azure_video_indexer_client import AzureVideoIndexerClient, VideoStatus

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


class TestAzureVideoIndexerClient(unittest.TestCase):
    def setUp(self):
        account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
        primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")

        self.azure_video_indexer_client = AzureVideoIndexerClient(account_id, primary_key)

    def test_index_video(self):
        new_video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        video_status = self.azure_video_indexer_client.index_video(new_video_url, 'new-video')
        print(video_status)
        assert isinstance(video_status, VideoStatus)
        assert isinstance(video_status.url, str)
        assert video_status.url == new_video_url
        assert video_status.state == "Uploaded"
        assert video_status.progress == 1

