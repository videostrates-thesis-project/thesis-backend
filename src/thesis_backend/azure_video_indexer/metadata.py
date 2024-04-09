from __future__ import annotations

from collections import defaultdict
from typing import NamedTuple, Final, Sequence

from rapidfuzz import fuzz
from rapidfuzz.distance import ScoreAlignment
from sortedcontainers import SortedKeyList

SEARCH_SCORE_CUTOFF: Final[int] = 80


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


class Match(NamedTuple):
    start: float
    end: float
    content: str
    highlighted: str
    confidence: float


class SearchResults(defaultdict[str, SortedKeyList[Match]]):
    @staticmethod
    def empty() -> SearchResults:
        return SearchResults(lambda: SortedKeyList(key=lambda x: -x.confidence))

    def add_match(self, url, segment: MetadataSegment, fuzz_result: ScoreAlignment) -> None:
        highlighted_content = self.__highlight_match(segment.content, fuzz_result.src_start, fuzz_result.src_end)
        match = Match(segment.start, segment.end, segment.content, highlighted_content, fuzz_result.score / 100)
        self[url].add(match)

    @staticmethod
    def __highlight_match(original: str, start: int, end: int) -> str:
        return f"{original[:start]}<mark>{original[start:end]}</mark>{original[end:]}"


class MetadataStore:
    def __init__(self) -> None:
        self.__collections: dict[str, MetadataCollection] = {}

    def add_video(self, url: str, metadata: MetadataCollection) -> None:
        self.__collections[url] = metadata

    def get_video(self, url: str) -> MetadataCollection | None:
        return self.__collections.get(url, None)

    def search(self, query: str, videos: list[SearchedVideo]) -> SearchResults:
        """
        Finds matches in all collections using rapidfuzz library, utilizing the Levenshtein distance.
        """
        search_text = query.lower()
        matches = SearchResults.empty()
        for collection_query in videos:
            collection = self.get_video(collection_query.url)
            if collection is None:
                continue
            for segment in collection.data:
                result = fuzz.partial_ratio_alignment(segment.content, search_text, score_cutoff=SEARCH_SCORE_CUTOFF)
                if result is not None:
                    matches.add_match(collection_query.url, segment, result)
        return matches
