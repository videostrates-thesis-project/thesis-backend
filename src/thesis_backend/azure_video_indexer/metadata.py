from __future__ import annotations
from typing import NamedTuple, Final, Sequence

from rapidfuzz import fuzz

SEARCH_CONFIDENCE_THRESHOLD: Final[float] = 70


class MetadataSegment(NamedTuple):
    start: float
    end: float
    content: str


class MetadataCollection:
    def __init__(self, metadata: Sequence[MetadataSegment]) -> None:
        data: Sequence[MetadataSegment] = sorted(metadata, key=lambda x: x.start)
        self.__data: Sequence[MetadataSegment] = list(
            map(lambda x: MetadataSegment(x.start, x.end, x.content.lower()), data))

    @property
    def data(self) -> Sequence[MetadataSegment]:
        return self.__data


class SearchedCollection(NamedTuple):
    name: str
    start: float
    end: float


class SearchQuery(NamedTuple):
    text: str
    collections: list[SearchedCollection]


class SearchResult(NamedTuple):
    collection: str
    match: MetadataSegment
    confidence: float


class MetadataStore:
    def __init__(self) -> None:
        self.__collections: dict[str, MetadataCollection] = {}

    def add_collection(self, name: str, metadata: MetadataCollection) -> None:
        self.__collections[name] = metadata

    def get_collection(self, name: str) -> MetadataCollection | None:
        return self.__collections.get(name, None)

    def search(self, query: SearchQuery) -> list[SearchResult]:
        """
        Finds matches in all collections using rapidfuzz library, utilizing the Levenshtein distance.
        """
        search_text = query.text.lower()
        matches: list[SearchResult] = []
        for collection_info in query.collections:
            collection = self.get_collection(collection_info.name)
            if collection is None:
                continue
            for segment in collection.data:
                ratio = fuzz.partial_ratio(search_text, segment.content)
                if ratio >= SEARCH_CONFIDENCE_THRESHOLD:
                    matches.append(SearchResult(collection_info.name, segment, ratio))
        return matches
