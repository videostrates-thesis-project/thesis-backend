import os
from dotenv import load_dotenv

from src.thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoIndexer, VideoIndexerToken

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


def test_get_access_token():
    account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
    primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")
    azure_video_indexer = VideoIndexerToken(account_id, primary_key)
    token = azure_video_indexer.token
    assert token is not None
    assert isinstance(token, str)


def test_upload_video():
    account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
    primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")
    azure_video_indexer = AzureVideoIndexer(account_id, primary_key)
    video_url = "https://storage.googleapis.com/videostrates.appspot.com/files/f90454fd-1616-4845-8252-f2978bab22a7.mp4"
    video_name = "sample-mp4-file"
    response = azure_video_indexer.upload_video(video_url, video_name)
    assert response is not None
    assert isinstance(response, dict)
    assert "id" in response
    assert "state" in response
    assert response["state"] == "Uploaded"


def test_get_video_index():
    account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
    primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")
    azure_video_indexer = AzureVideoIndexer(account_id, primary_key)
    video_id = "84505873fd"
    response = azure_video_indexer.get_video_index(video_id)
    assert response is not None
    assert isinstance(response, dict)
    assert "id" in response
    assert response["id"] == video_id
