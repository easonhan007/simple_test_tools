# support all faker methods
# https://faker.readthedocs.io/en/master/locales/zh_CN.html
# USAGE: 
# export FLASK_APP=mock.py flask run
# windows: set FLASK_APP=mock.py flask run



from flask import Flask, jsonify, request
from faker import Faker
import json
app = Flask(__name__)
fake = Faker('zh_CN')

def load_config(file_name="./config.json"):
    try:
        with open(file_name) as f:
            return json.loads(f.read())
    except:
        exit("can not load config file")

conf = load_config()

@app.route('/')
@app.route('/<path:url_path>')
def index(url_path="", methods=['GET', 'POST']):
    path = "/" + url_path
    if path in conf and request.method == conf[path]['method'].upper() :
        return jsonify(build_response(conf[path]['response']))
    return "/%s is not defined " %(url_path)

def build_response(res):
    size = int(res['length'])
    if size == 1:
        response = build_obj(res['content'])
    else:
        response = []
        for i in range(0, size):
            response.append(build_obj(res['content']))
    return response

def build_obj(content):
    obj = {}
    for each in [item for item in content.split(';')]:
        k, v = each.split(':')
        if '(' in v and ')' in v:
            obj[k] = eval("fake.%s" %(v))
        else:
            obj[k] = eval("fake.%s()" %(v))
    return obj
        
        
            

