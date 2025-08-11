import fakeredis
from app.api.trending_api import add_word_to_trending, trending_words

def test_trending():
    r = fakeredis.FakeRedis()

    word = "origin"
    add_word_to_trending(word, r)

    trending = r.get("trending")
    assert trending

    data = trending_words(r)
    assert word in data.trending
    assert data.trending[word] == 1

def test_multi_words():
    r = fakeredis.FakeRedis()
    words = ["origin", "patient", "notice"]

    for w in words:
        add_word_to_trending(w, r)
        
    add_word_to_trending("safe", r)
    add_word_to_trending("safe", r)
    data = trending_words(r)

    assert data.trending["safe"] == 2
    assert len(data.trending) == 4
