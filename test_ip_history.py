from app.api.ip_history_api import add_word_to_history, history_page, export_history
import fakeredis

def test_history():
    r = fakeredis.FakeRedis()
    ip = "127.0.0.1"
    word = "serendipity"
    
    add_word_to_history(ip, word, r)
    page = history_page(ip, r, limit=5, page=1)
    
    assert page["total"] == 1
    assert page["data"][0]["word"] == word

def test_export_history_json():
    r = fakeredis.FakeRedis()
    ip = "127.0.0.1"
    add_word_to_history(ip, "jsonfile", r)
    
    exported = export_history(ip, r, format="json")
    assert isinstance(exported, list)
    assert exported[0]["word"] == "jsonfile"

def test_export_history_csv():
    r = fakeredis.FakeRedis()
    ip = "127.0.0.1"
    add_word_to_history(ip, "csvfile", r)
    
    exported = export_history(ip, r, format="csv")
    assert "csvfile" in exported
    assert "time,word" in exported

def test_export_history_txt():
    r = fakeredis.FakeRedis()
    ip = "127.0.0.1"
    add_word_to_history(ip, "txtfile", r)
    
    exported = export_history(ip, r, format="txt")
    assert "txtfile" in exported
    assert "-" in exported 