from __future__ import annotations

import os

from flask import Blueprint

from thesis_backend.azure_video_indexer.azure_video_indexer import AzureVideoIndexer
from thesis_backend.azure_video_indexer.metadata import SearchedVideo, Match
from thesis_backend.schema import AzureVideoIndexerIndexSchema, AzureVideoIndexerStatusSchema, \
    AzureVideoIndexerSearchSchema
from thesis_backend.utils.with_request_data import with_request_data

bp = Blueprint("azure_video_indexer", __name__)

account_id = os.environ.get("VIDEO_INDEXER_ACCOUNT_ID")
primary_key = os.environ.get("VIDEO_INDEXER_PRIMARY_KEY")

azure_video_indexer = AzureVideoIndexer(account_id, primary_key)
if account_id is not None:
    print("Initializing Azure Video Indexer...")
    azure_video_indexer.get_videos_status([])
    print("Azure Video Indexer initialized")


@bp.post("/azure_video_indexer/index")
@with_request_data(AzureVideoIndexerIndexSchema())
def upload_video(request_data) -> tuple[dict[str, str], int]:
    try:
        video_status = azure_video_indexer.upload_video(request_data.get("url"), request_data.get("name"))
    except Exception as e:
        return {"error": "Failed to upload video", "message": str(e)}, 500
    return video_status._asdict(), 200


@bp.post("/azure_video_indexer/status")
@with_request_data(AzureVideoIndexerStatusSchema())
def get_videos_status(request_data) -> tuple[dict[str, dict[str, str]], int] | tuple[dict[str, str], int]:
    try:
        videos_status = azure_video_indexer.get_videos_status(request_data.get("urls"))
    except Exception as e:
        return {"error": "Failed to get video status", "message": str(e)}, 500

    response = {video.url: video._asdict() for video in videos_status.values()}
    return response, 200


@bp.post("/azure_video_indexer/search")
@with_request_data(AzureVideoIndexerSearchSchema())
def search_videos(request_data) -> tuple[list[dict[str, str | dict]], int] | tuple[dict[str, str], int]:
    videos = [SearchedVideo(**video) for video in request_data.get("videos")]
    try:
        matches = azure_video_indexer.search(request_data.get("query"), videos)
    except Exception as e:
        return {"error": "Failed to search videos", "message": str(e)}, 500
    m: Match
    response = {url: [m._asdict() for m in video_match] for url, video_match in matches.items()}
    return response, 200
