from __future__ import annotations
from typing import NamedTuple, Final, Sequence

from rapidfuzz import fuzz

SEARCH_CONFIDENCE_THRESHOLD: Final[float] = 0.7


class MetadataSegment(NamedTuple):
    start: float
    end: float
    content: str
    confidence: float = 1


class MetadataCollection:
    def __init__(self, metadata: Sequence[MetadataSegment]) -> None:
        data: Sequence[MetadataSegment] = sorted(metadata, key=lambda x: x.start)
        self.__data: Sequence[MetadataSegment] = [x._replace(content=x.content.lower()) for x in data]

    @property
    def data(self) -> Sequence[MetadataSegment]:
        return self.__data


class SearchedVideo(NamedTuple):
    url: str
    start: float
    end: float


class SearchQuery(NamedTuple):
    text: str
    videos: list[SearchedVideo]


class SearchResult(NamedTuple):
    video_url: str
    match: MetadataSegment
    confidence: float


class MetadataStore:
    def __init__(self) -> None:
        self.__collections: dict[str, MetadataCollection] = {}

    def add_video(self, url: str, metadata: MetadataCollection) -> None:
        self.__collections[url] = metadata

    def get_video(self, url: str) -> MetadataCollection | None:
        return self.__collections.get(url, None)

    def search(self, query: SearchQuery) -> Sequence[SearchResult]:
        """
        Finds matches in all collections using rapidfuzz library, utilizing the Levenshtein distance.
        """
        search_text = query.text.lower()
        matches: list[SearchResult] = []
        for collection_query in query.videos:
            collection = self.get_video(collection_query.url)
            if collection is None:
                continue
            for segment in collection.data:
                ratio = fuzz.partial_ratio(search_text, segment.content) / 100
                if ratio >= SEARCH_CONFIDENCE_THRESHOLD:
                    matches.append(SearchResult(collection_query.url, segment, ratio))
        return matches
