import pytest
from app.api.dictionary_api import word_info
from app.models.models import WordResponse
import fakeredis
import json

@pytest.fixture
def fake_redis():
    return fakeredis.FakeRedis()

def test_word_info(fake_redis):
    word = "serendipity"
    meaning_data = {
        "word": word,
        "phonetic": "/ˌser.ənˈdɪp.ə.ti/",
        "meanings": [
            {
                "noun": [
                    "The occurrence of fortunate events by chance."
                ]
            }
        ],
        "tags": ["noun"],
        "title": None,
        "message": None,
        "resolution": None
    }
    fake_redis.set(f"word:{word}", json.dumps(meaning_data))
    response = word_info(word, fake_redis)

    assert isinstance(response, WordResponse)
    assert response.word == word
    assert response.meanings == meaning_data["meanings"]
    assert response.phonetic == meaning_data["phonetic"]
    assert response.tags == meaning_data["tags"]

def test_word_info_not_found(fake_redis):
    word = "elma"
    response = word_info(word, fake_redis)

    assert response.word == "Word Not Found"
    assert response.message is not None

