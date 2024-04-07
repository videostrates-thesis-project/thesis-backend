import unittest

from src.thesis_backend.azure_video_indexer.metadata import MetadataCollection, MetadataStore, MetadataSegment, \
    SearchedVideo

COLLECTION_1 = [
    MetadataSegment(3.2, 8.32, "Oh, you cute little corny, was person that name bonus point."),
    MetadataSegment(12.12, 14.36, "Can't believe we got stuck with a tree hugger."),
    MetadataSegment(14.56, 18.28, "If I have to hear the Latin name for one more animal, I swear I'm going to kill."),
    MetadataSegment(18.92, 23, "Sugar Bun While she does all the work, we'll have all the fun."),
    MetadataSegment(23.12, 25.64, "Yeah, and get wasted out of our minds"),
]

COLLECTION_2 = [
    MetadataSegment(27.88, 31.76, "Come on, team, we mustn't dilly dally when there's so much nature to see."),
    MetadataSegment(32.36, 36.32, "I was thinking we should call our class project Fun Guys in a Forest."),
    MetadataSegment(37.44, 37.8, "Get it?"),
    MetadataSegment(38.12, 41.16, "Because we're a group of fun guys."),
    MetadataSegment(41.4, 44.16, "And also fungi."),
]


class TestMetadata(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata_store = MetadataStore()
        self.metadata_collection_1 = MetadataCollection(COLLECTION_1)
        self.metadata_collection_2 = MetadataCollection(COLLECTION_2)
        self.metadata_store.add_video("sprite_fright_1_url", self.metadata_collection_1)
        self.metadata_store.add_video("sprite_fright_2_url", self.metadata_collection_2)

    def test_get_collection(self):
        assert self.metadata_store.get_video("sprite_fright_1_url") == self.metadata_collection_1
        assert self.metadata_store.get_video("sprite_fright_2_url") == self.metadata_collection_2

    def test_search(self):
        query = "fun guys"
        videos = [SearchedVideo("sprite_fright_1_url", 0, 60), SearchedVideo("sprite_fright_2_url", 0, 60)]
        search_results = self.metadata_store.search(query, videos)
        print(search_results)
        assert len(search_results) == 2
        assert search_results[0].url == "sprite_fright_2_url"
        assert search_results[0].match.content == COLLECTION_2[1].content.lower()
        assert search_results[0].confidence == 1

        assert search_results[1].url == "sprite_fright_2_url"
        assert search_results[1].match.content == COLLECTION_2[3].content.lower()
        assert search_results[1].confidence == 1
