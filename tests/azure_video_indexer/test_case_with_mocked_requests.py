from abc import ABC
from unittest.mock import patch, MagicMock
from tests.azure_video_indexer.example_video_index_response import EXAMPLE_VIDEO_INDEX_RESPONSE, EXISTING_VIDEO_URL, \
    EXISTING_VIDEO_ID
from tests.azure_video_indexer.example_video_list_response import EXAMPLE_VIDEO_LIST_RESPONSE


class TestCaseWithMockedRequests(ABC):
    mock_requests_get = None
    mock_requests_post = None
    patcher_requests_get = None
    patcher_requests_post = None

    existing_video_url = EXISTING_VIDEO_URL
    existing_video_id = EXISTING_VIDEO_ID
    invalid_video_url = "invalid_url"

    @classmethod
    def setUpClass(cls):
        cls.patcher_requests_get = patch('requests.get')
        cls.mock_requests_get = cls.patcher_requests_get.start()
        cls.mock_requests_get.side_effect = cls.mocked_get_response

        cls.patcher_requests_post = patch('requests.post')
        cls.mock_requests_post = cls.patcher_requests_post.start()
        cls.mock_requests_post.side_effect = cls.mocked_post_response

    @staticmethod
    def mocked_get_response(url: str, *args, **kwargs):
        if url.endswith('/AccessToken'):
            return MagicMock(json=lambda: 'mocked_access_token')
        elif url.endswith('/Index'):
            return MagicMock(json=lambda: EXAMPLE_VIDEO_INDEX_RESPONSE)
        elif url.endswith('/Videos'):
            return MagicMock(json=lambda: EXAMPLE_VIDEO_LIST_RESPONSE)
        else:
            raise ValueError(f"Unexpected URL has been called: {url}")

    @staticmethod
    def mocked_post_response(url: str, params: dict[str, str], *args, **kwargs):
        if url.endswith('/Videos'):
            if params['videoUrl'] == TestCaseWithMockedRequests.invalid_video_url:
                return MagicMock(json=lambda: {
                    "ErrorType": "InvalidInput",
                    "Message": "The input is invalid."
                })
            return MagicMock(json=lambda: {
                "id": '323fad75d2',
                "description": params['videoUrl'],
                "state": "Uploaded",
                "processingProgress": "1%"
            })
        else:
            raise ValueError(f"Unexpected URL has been called: {url}")

    @classmethod
    def tearDownClass(cls):
        cls.patcher_requests_get.stop()
        cls.patcher_requests_post.stop()
