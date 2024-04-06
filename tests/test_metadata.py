from src.thesis_backend.azure_video_indexer.metadata import MetadataCollection, MetadataStore, MetadataSegment, \
    SearchQuery, SearchedCollection

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


def test_add_get_collection():
    metadata_store = MetadataStore()
    metadata_collection_1 = MetadataCollection(COLLECTION_1)
    metadata_collection_2 = MetadataCollection(COLLECTION_2)
    metadata_store.add_collection("Sprite Fright 1", metadata_collection_1)
    metadata_store.add_collection("Sprite Fright 2", metadata_collection_2)
    assert metadata_store.get_collection("Sprite Fright 1") == metadata_collection_1
    assert metadata_store.get_collection("Sprite Fright 2") == metadata_collection_2


def test_search():
    metadata_store = MetadataStore()
    metadata_collection_1 = MetadataCollection(COLLECTION_1)
    metadata_collection_2 = MetadataCollection(COLLECTION_2)
    metadata_store.add_collection("Sprite Fright 1", metadata_collection_1)
    metadata_store.add_collection("Sprite Fright 2", metadata_collection_2)
    search_query = SearchQuery("fun guys", [SearchedCollection("Sprite Fright 1", 0, 60),
                                            SearchedCollection("Sprite Fright 2", 0, 60)])
    search_results = metadata_store.search(search_query)
    print(search_results)
    assert len(search_results) == 2
    assert search_results[0].collection == "Sprite Fright 2"
    assert search_results[0].match.content == COLLECTION_2[1].content.lower()
    assert search_results[0].confidence == 100

    assert search_results[1].collection == "Sprite Fright 2"
    assert search_results[1].match.content == COLLECTION_2[3].content.lower()
    assert search_results[1].confidence == 100
