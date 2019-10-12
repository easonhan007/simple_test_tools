import requests
def dict_merge(a, b):
    c = a.copy()
    c.update(b)
    return c

class TestSuit:
    
    def __init__(self, debug=False):
        self._debug_flag = debug
        self._resp = None
        self._headers = {}
        self._cookie = {}
        self._timeout = None
        self._method = ''
        self._url = ''
        self._params = None
        self._kwargs = {}
        self._json_res = None

    def request(self, method, url, **kwargs):
        return requests.request(method, url, **kwargs)        

    def get(self,url, params=None, **kwargs):
        self._url = url
        self._method = 'get'
        self._params = params
        self._kwargs = kwargs
        return self

    def send(self):
        if self._debug_flag:
            print(self._resp)
            print(self._headers)
            print(self._cookie)
            print(self._timeout)
            print(self._method)
            print(self._url)
            print(self._params)
            print(self._kwargs)
        self._resp = self.request(self._method, self._url)
        if self._debug_flag:
            print(self._resp)
        return self

    def headers(self, **kwargs):
        self._headers = dict_merge(self._headers,kwargs)
        return self
    
    def cookies(self, **kwargs):
        self._cookies = dict_merge(self._cookies,kwargs)
        return self

    def timeout(self, value):
        self._timeout = value        
        return self

    def json_assert_eq(self, **kwargs):
        self._validate_resp()
        for k, v in kwargs.items():
            print(k,v)
            assert self._json_res[k] == v
        return self

    def json_assert_list_eq(self, index, **kwargs):
        self._validate_resp()
        self._parse_json()
        if isinstance(self._json_res, list) and type(index) == int:
            for k, v in kwargs.items():
                print(k,v)
                assert self._json_res[index][k] == v
            return self
        else:
            pass #just ignore this assertion
        return self
    
    def json_assert_len(self, length):
        self._validate_resp()
        self._parse_json()
        if type(length) == int:
            json_length = len(self._json_res)
            assert  json_length == length, "expect %d got %d" %(length, json_length)
        else:
            pass
    
    def json_assert_has_key(self, key):
        self._validate_resp()
        self._parse_json()
        assert key in self._json_res

    def _parse_json(self):
        if self._json_res is None:
            self._json_res = self._resp.json()
            if self._debug_flag:
                print(self._json_res)

    def _validate_resp(self):
        if self._debug_flag:
            print(type(self._resp))
        if self._resp is None:
            raise("No response")
        if not isinstance(self._resp, requests.models.Response):
            raise("Response is not a requests response")
            


        
        