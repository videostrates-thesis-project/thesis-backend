EXISTING_VIDEO_URL = "example.com/video1.mp4"
EXISTING_VIDEO_ID = "323fad75d2"

EXAMPLE_VIDEO_INDEX_RESPONSE = {
    "partition": None,
    "description": EXISTING_VIDEO_URL,
    "privacyMode": "Private",
    "state": "Processed",
    "accountId": "account_id",
    "id": EXISTING_VIDEO_ID,
    "name": "SpriteFright 5s",
    "userName": "User 1",
    "created": "2024-04-08T20:10:34.9933333+00:00",
    "isOwned": True,
    "isEditable": False,
    "isBase": True,
    "durationInSeconds": 5,
    "duration": "0:00:05.2",
    "summarizedInsights": None,
    "videos": [
        {
            "accountId": "account_id",
            "id": "53c7fca6b5",
            "state": "Processed",
            "moderationState": "OK",
            "reviewState": "None",
            "privacyMode": "Private",
            "processingProgress": "100%",
            "failureMessage": "",
            "externalId": None,
            "externalUrl": None,
            "metadata": None,
            "insights": {
                "version": "1.0.0.0",
                "duration": "0:00:05.2",
                "sourceLanguage": "en-US",
                "sourceLanguages": [
                    "en-US"
                ],
                "language": "en-US",
                "languages": [
                    "en-US"
                ],
                "transcript": [
                    {
                        "id": 1,
                        "text": "Hello Mr.",
                        "confidence": 0.6881,
                        "speakerId": 1,
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:02.12",
                                "start": "0:00:01.24",
                                "end": "0:00:02.12"
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "text": "Snail.",
                        "confidence": 0.6895,
                        "speakerId": 1,
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:02.12",
                                "adjustedEnd": "0:00:02.72",
                                "start": "0:00:02.12",
                                "end": "0:00:02.72"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "text": "Oh, you cute little corny was spelled.",
                        "confidence": 0.5049,
                        "speakerId": 1,
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:03.2",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:03.2",
                                "end": "0:00:05.16"
                            }
                        ]
                    }
                ],
                "topics": [
                    {
                        "id": 1,
                        "name": "Anime",
                        "referenceId": "Movies, Tv and Entertainment/Entertainment/Anime",
                        "referenceType": "VideoIndexer",
                        "iptcName": "arts, culture, entertainment and media/arts and entertainment/cartoon",
                        "confidence": 0.6491,
                        "iabName": "Movies",
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:01.24",
                                "end": "0:00:05.16"
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "name": "Manga",
                        "referenceId": "Movies, Tv and Entertainment/Literature/Manga",
                        "referenceType": "VideoIndexer",
                        "iptcName": "arts, culture, entertainment and media/arts and entertainment/cartoon",
                        "confidence": 0.5834,
                        "iabName": "Movies",
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:01.24",
                                "end": "0:00:05.16"
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "name": "Movies",
                        "referenceId": "Movies, Tv and Entertainment/Movies",
                        "referenceType": "VideoIndexer",
                        "iptcName": "arts, culture, entertainment and media/arts and entertainment/movies",
                        "confidence": 0.5796,
                        "iabName": "Movies",
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:01.24",
                                "end": "0:00:05.16"
                            }
                        ]
                    },
                    {
                        "id": 4,
                        "name": "Music",
                        "referenceId": "Music",
                        "referenceType": "VideoIndexer",
                        "iptcName": "arts, culture, entertainment and media/arts and entertainment/music",
                        "confidence": 0.5053,
                        "iabName": "Music and Audio",
                        "language": "en-US",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:01.24",
                                "end": "0:00:05.16"
                            }
                        ]
                    }
                ],
                "faces": [
                    {
                        "id": 1000,
                        "name": "Unknown #1",
                        "confidence": 0,
                        "description": None,
                        "thumbnailId": "86216f8e-b35b-48e3-ac0c-c8daaab24351",
                        "title": None,
                        "imageUrl": None,
                        "highQuality": True,
                        "thumbnails": [
                            {
                                "id": "641d6edc-273f-490c-96ae-2dbdc996674f",
                                "fileName": "FaceInstanceThumbnail_641d6edc-273f-490c-96ae-2dbdc996674f.jpg",
                                "instances": [
                                    {
                                        "adjustedStart": "0:00:01.4",
                                        "adjustedEnd": "0:00:01.4333333",
                                        "start": "0:00:01.4",
                                        "end": "0:00:01.4333333"
                                    }
                                ]
                            },
                            {
                                "id": "bc566c58-f226-4b9e-86b6-2b2edaff0332",
                                "fileName": "FaceInstanceThumbnail_bc566c58-f226-4b9e-86b6-2b2edaff0332.jpg",
                                "instances": [
                                    {
                                        "adjustedStart": "0:00:03.2666666",
                                        "adjustedEnd": "0:00:03.2999999",
                                        "start": "0:00:03.2666666",
                                        "end": "0:00:03.2999999"
                                    }
                                ]
                            }
                        ],
                        "instances": [
                            {
                                "thumbnailsIds": [
                                    "641d6edc-273f-490c-96ae-2dbdc996674f",
                                    "bc566c58-f226-4b9e-86b6-2b2edaff0332"
                                ],
                                "adjustedStart": "0:00:01.3",
                                "adjustedEnd": "0:00:05.2",
                                "start": "0:00:01.3",
                                "end": "0:00:05.2"
                            }
                        ]
                    }
                ],
                "labels": [
                    {
                        "id": 1,
                        "name": "cartoon",
                        "language": "en-US",
                        "instances": [
                            {
                                "confidence": 0.9626,
                                "adjustedStart": "0:00:02",
                                "adjustedEnd": "0:00:02.0333333",
                                "start": "0:00:02",
                                "end": "0:00:02.0333333"
                            }
                        ]
                    }
                ],
                "scenes": [
                    {
                        "id": 1,
                        "instances": [
                            {
                                "adjustedStart": "0:00:00",
                                "adjustedEnd": "0:00:05.2",
                                "start": "0:00:00",
                                "end": "0:00:05.2"
                            }
                        ]
                    }
                ],
                "shots": [
                    {
                        "id": 1,
                        "tags": [
                            "CloseUp",
                            "LeftFace"
                        ],
                        "keyFrames": [
                            {
                                "id": 1,
                                "instances": [
                                    {
                                        "thumbnailId": "0c8527a6-c0ae-49c3-a377-365617973265",
                                        "adjustedStart": "0:00:00.2",
                                        "adjustedEnd": "0:00:00.2333333",
                                        "start": "0:00:00.2",
                                        "end": "0:00:00.2333333"
                                    }
                                ]
                            },
                            {
                                "id": 2,
                                "instances": [
                                    {
                                        "thumbnailId": "1f601b1a-6227-4196-95ec-12bc89bd3ea5",
                                        "adjustedStart": "0:00:01.3666667",
                                        "adjustedEnd": "0:00:01.4",
                                        "start": "0:00:01.3666667",
                                        "end": "0:00:01.4"
                                    }
                                ]
                            }
                        ],
                        "instances": [
                            {
                                "adjustedStart": "0:00:00",
                                "adjustedEnd": "0:00:05.2",
                                "start": "0:00:00",
                                "end": "0:00:05.2"
                            }
                        ]
                    }
                ],
                "sentiments": [
                    {
                        "id": 1,
                        "averageScore": 0.5,
                        "sentimentType": "Neutral",
                        "instances": [
                            {
                                "adjustedStart": "0:00:00",
                                "adjustedEnd": "0:00:05.2",
                                "start": "0:00:00",
                                "end": "0:00:05.2"
                            }
                        ]
                    }
                ],
                "blocks": [
                    {
                        "id": 0,
                        "instances": [
                            {
                                "adjustedStart": "0:00:00",
                                "adjustedEnd": "0:00:05.2",
                                "start": "0:00:00",
                                "end": "0:00:05.2"
                            }
                        ]
                    }
                ],
                "speakers": [
                    {
                        "id": 1,
                        "name": "Speaker #1",
                        "instances": [
                            {
                                "adjustedStart": "0:00:01.24",
                                "adjustedEnd": "0:00:02.12",
                                "start": "0:00:01.24",
                                "end": "0:00:02.12"
                            },
                            {
                                "adjustedStart": "0:00:02.12",
                                "adjustedEnd": "0:00:02.72",
                                "start": "0:00:02.12",
                                "end": "0:00:02.72"
                            },
                            {
                                "adjustedStart": "0:00:03.2",
                                "adjustedEnd": "0:00:05.16",
                                "start": "0:00:03.2",
                                "end": "0:00:05.16"
                            }
                        ]
                    }
                ],
                "textualContentModeration": {
                    "id": 0,
                    "bannedWordsCount": 0,
                    "bannedWordsRatio": 0,
                    "instances": []
                },
                "statistics": {
                    "correspondenceCount": 0,
                    "speakerTalkToListenRatio": {
                        "1": 1
                    },
                    "speakerLongestMonolog": {
                        "1": 3
                    },
                    "speakerNumberOfFragments": {
                        "1": 2
                    },
                    "speakerWordCount": {
                        "1": 10
                    }
                }
            },
            "thumbnailId": "46ad81eb-086a-44ea-920c-256f21a0931d",
            "width": 852,
            "height": 480,
        }
    ],
    "videosRanges": [
        {
            "videoId": "53c7fca6b5",
            "range": {
                "start": "0:00:00",
                "end": "0:00:05.2"
            }
        }
    ]
}