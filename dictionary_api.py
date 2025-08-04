import requests
from models import WordResponse
import redis
import json

def word_info(word: str):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    cached_word = r.get(f"word:{word}")
    if cached_word:
        return WordResponse(**json.loads(cached_word))

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        resp = requests.get(url)
        data = resp.json()

        if not isinstance(data, list):
            new_response = WordResponse(
                word="Word Not Found",
                phonetic="Phonetic Not Found.",
                meanings=[{"unknown": ["Meanings Not Found."]}],
                tags = ["Tags Not Found."],
                title="Definition Not Found.",
                message="We couldn't locate a definition for the word you entered.",
                resolution="Please try searching a different word."
            )
            r.set(f"word:{word}", json.dumps(new_response.dict()))
            return new_response

        def find_phonetic(data):
            for phtic in data:
                if "text" in phtic:
                    return phtic["text"]
            return "Phonetic Not Found."

        def find_meanings(data):
            tags = {}
            for meaning in data.get('meanings', []):
                tag = meaning.get("partOfSpeech", "mean")
                meanings = []
                for defn in meaning.get('definitions', []):
                    definition = defn.get('definition')
                    if definition:
                        meanings.append(definition)
                    else:
                        meanings.append("Meanings Not Found.")
                tags[tag] = meanings
            meanings = [{tag: defns} for tag, defns in tags.items()]
            return meanings, list(tags.keys())

        meanings, tags = find_meanings(data[0])
        phonetic = find_phonetic(data[0].get("phonetics", []))

        new_response = WordResponse(
            word=word,
            phonetic=phonetic,
            meanings=meanings,
            tags=tags,
            title=None,
            message=None,
            resolution=None
        )

        r.set(f"word:{word}", json.dumps(new_response.dict()))
        return new_response

    except Exception:
        return WordResponse(
            word=word,
            phonetic=None,
            meanings=None,
            tags=None,
            title="Network Error",
            message="Unable to connect to the dictionary API service.",
            resolution="Please check your internet connection or try again later."
        )