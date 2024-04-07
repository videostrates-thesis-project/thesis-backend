import unittest
from unittest.mock import patch
from flask import Flask, json
from src.thesis_backend.api.azure_video_indexer import bp
from src.thesis_backend.azure_video_indexer.azure_video_indexer import VideoStatus
from src.thesis_backend.azure_video_indexer.metadata import SearchResult, MetadataSegment


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)
        self.client = self.app.test_client()

    @patch("src.thesis_backend.api.azure_video_indexer.azure_video_indexer")
    def test_upload_video_success(self, mock_azure_video_indexer):
        mock_azure_video_indexer.upload_video.return_value = VideoStatus(
            "example_id",
            "example_url",
            "Processing",
            0)

        request_data = {"url": "example_url", "name": "example_name"}
        response = self.client.post("/azure_video_indexer/index", json=request_data)

        assert response.status_code == 200
        assert json.loads(response.data) == {"id": "example_id", "url": "example_url", "state": "Processing",
                                             "progress": 0}
        assert mock_azure_video_indexer.upload_video.call_count == 1

    def test_upload_video_invalid_request(self):
        # Define invalid request data (missing 'url' field)
        request_data = {
            "name": "example_name"
        }
        response = self.client.post("/azure_video_indexer/index", json=request_data)

        assert response.status_code == 400
        assert "url" in json.loads(response.data)["error"]

    @patch("src.thesis_backend.api.azure_video_indexer.azure_video_indexer")
    def test_upload_video_with_exception(self, mock_azure_video_indexer):
        mock_azure_video_indexer.upload_video.side_effect = Exception("Unknown error occurred")

        request_data = {"url": "example_url", "name": "example_name"}
        response = self.client.post("/azure_video_indexer/index", json=request_data)

        assert response.status_code == 500
        assert json.loads(response.data) == {"error": "Failed to upload video", "message": "Unknown error occurred"}

    @patch("src.thesis_backend.api.azure_video_indexer.azure_video_indexer")
    def test_get_videos_status_success(self, mock_azure_video_indexer):
        video_status = VideoStatus(
            "example_id",
            "example_url",
            "Processing",
            0)
        mock_azure_video_indexer.get_videos_status.return_value = [video_status]

        request_data = {"urls": ["example_url"]}
        response = self.client.get("/azure_video_indexer/status", json=request_data)

        assert response.status_code == 200
        assert json.loads(response.data) == {"example_url": {
            "id": "example_id",
            "url": "example_url",
            "state": "Processing",
            "progress": 0
        }}
        assert mock_azure_video_indexer.get_videos_status.call_count == 1

    def test_get_videos_status_invalid_request(self):
        # Define invalid request data (missing 'urls' field)
        request_data = {"url": ["example_url"]}
        response = self.client.get("/azure_video_indexer/status", json=request_data)

        assert response.status_code == 400
        assert "urls" in json.loads(response.data)["error"]

    @patch("src.thesis_backend.api.azure_video_indexer.azure_video_indexer")
    def test_search_videos_success(self, mock_azure_video_indexer):
        mock_azure_video_indexer.search.return_value = [
            SearchResult("example_url", MetadataSegment(0, 2, "some_text", 0.8), 0.98)]
        # Define valid request data
        request_data = {"query": "example_query", "videos": [{"url": "example_url", "start": 0, "end": 60}]}
        response = self.client.get("/azure_video_indexer/search", json=request_data)
        assert response.status_code == 200
        assert json.loads(response.data) == [
            {'url': 'example_url', 'match': {'start': 0, 'end': 2, 'content': 'some_text', 'confidence': 0.8},
             'confidence': 0.98}]

    def test_search_videos_missing_query(self):
        # Define invalid request data (missing 'query' field)
        request_data = {"videos": [{"url": "example_url", "start": 0, "end": 60}]}
        response = self.client.get("/azure_video_indexer/search", json=request_data)

        assert response.status_code == 400
        assert "query" in json.loads(response.data)["error"]

    def test_search_videos_missing_start(self):
        # Define invalid request data (missing 'query' field)
        request_data = {"query": "example_query", "videos": [{"url": "example_url", "end": 60}]}
        response = self.client.get("/azure_video_indexer/search", json=request_data)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "videos" in data["error"]
        assert "start" in data["error"]["videos"]['0']
