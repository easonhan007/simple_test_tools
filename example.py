from api import TestSuit

def test_v2ex_api():
    ts = TestSuit()
    ts.get('https://www.v2ex.com/api/topics/hot.json').send().json_assert_len(5)