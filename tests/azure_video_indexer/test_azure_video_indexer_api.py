import unittest
from flask import Flask, json
from src.thesis_backend.api.azure_video_indexer import bp
from tests.azure_video_indexer.test_case_with_mocked_requests import TestCaseWithMockedRequests


class TestAPI(TestCaseWithMockedRequests, unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)
        self.client = self.app.test_client()

    def test_upload_video_success(self):
        new_video_url = "new-video.mp4"
        request_data = {"url": new_video_url, "name": "example_name"}
        response = self.client.post("/azure_video_indexer/index", json=request_data)

        assert response.status_code == 200
        video = json.loads(response.data)
        assert video["url"] == new_video_url
        assert video["state"] == "Uploaded"
        assert video["progress"] == 1

    def test_get_videos_status(self):
        request_data = {"urls": [self.existing_video_url]}
        response = self.client.post("/azure_video_indexer/status", json=request_data)

        assert response.status_code == 200
        data = json.loads(response.data)
        print(data)
        assert self.existing_video_url in data
        assert data[self.existing_video_url]["state"] == "Processed"
        assert data[self.existing_video_url]["url"] == self.existing_video_url

    def test_get_videos_status_invalid_request(self):
        request_data = {"url": [self.invalid_video_url]}
        response = self.client.post("/azure_video_indexer/status", json=request_data)
        assert response.status_code == 400
        assert "urls" in json.loads(response.data)["error"]

    def test_search_videos(self):
        request_data = {"query": "cute little", "videos": [{"url": self.existing_video_url, "start": 0, "end": 60}]}
        response = self.client.post("/azure_video_indexer/search", json=request_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        for url, result in data.items():
            assert url == self.existing_video_url
            for match in result:
                assert isinstance(match["start"], float)
                assert isinstance(match["end"], float)
                assert isinstance(match["content"], str)
                assert isinstance(match["highlighted"], str)
                assert isinstance(match["confidence"], float)
                assert 0 <= match["confidence"] <= 1

    def test_search_videos_missing_query(self):
        # Define invalid request data (missing 'query' field)
        request_data = {"videos": [{"url": "example_url", "start": 0, "end": 60}]}
        response = self.client.post("/azure_video_indexer/search", json=request_data)

        assert response.status_code == 400
        assert "query" in json.loads(response.data)["error"]

    def test_search_videos_empty_list(self):
        # Define invalid request data (missing 'query' field)
        request_data = {"query": "example_query", "videos": []}
        response = self.client.post("/azure_video_indexer/search", json=request_data)
        print(json.loads(response.data))

        assert response.status_code == 400
        assert "videos" in json.loads(response.data)["error"]

    def test_search_videos_missing_start(self):
        # Define invalid request data (missing 'query' field)
        request_data = {"query": "example_query", "videos": [{"url": "example_url", "end": 60}]}
        response = self.client.post("/azure_video_indexer/search", json=request_data)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "videos" in data["error"]
        assert "start" in data["error"]["videos"]['0']
