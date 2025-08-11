import fakeredis
import json
from app.api.word_day_api import word_of_the_day

def test_existing_word():
    r = fakeredis.FakeRedis()

    word = "bright"
    word_data = {
        "word": word,
        "meaning": "Giving off a lot of light.",
        "tags": ["adjective"]
    }
    r.set(b"word_of_the_day", word.encode())  
    r.set(b"random_word:" + word.encode(), json.dumps(word_data))
    
    result = word_of_the_day(r)

    assert result.word == word
    assert result.definition == word_data["meaning"]
    assert "adjective" in result.tags

def test_new_word():
    r = fakeredis.FakeRedis()

    word_data = {
        "word": "divide",
        "meaning": "To separate into parts or groups.",
        "tags": ["adjective"]
    }

    r.sadd("words_unused", json.dumps(word_data))
    
    result = word_of_the_day(r)

    assert result.word == "divide"
    assert result.definition == "To separate into parts or groups."
    assert "adjective" in result.tags
    assert r.get("word_of_the_day") == b"divide"
