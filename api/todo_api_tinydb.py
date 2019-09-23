# pip install flask
# pip install tinydb

from flask import Flask, g, jsonify, request
from tinydb import TinyDB, Query
import uuid
import re

DB = './tasks.json'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = TinyDB(DB)
    return db

app = Flask(__name__)

@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    return jsonify(db.all())

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    db = get_db()
    task = request.json
    if task is not None and task['title']:
        task_data = {'title': task['title'], 'done': False, 'id': str(uuid.uuid4())}
        db.insert(task_data)
        return jsonify({'id': task_data['id']})
    else:
        return jsonify({'msg': 'title is required'}), 442

@app.route("/api/v1/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    db = get_db()
    result = db.search(Query().id == task_id)
    if len(result) >= 1:
        return jsonify(result[0])
    else:
        return jsonify({'msg': 'NOT FOUND'}), 404

@app.route("/api/v1/tasks/fragment/<fragment>", methods=["GET"])
def get_task_with(fragment):
    db = get_db()
    result = db.search(Query().id.matches(fragment, flags=re.IGNORECASE))
    return jsonify(result)

@app.route("/api/v1/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    db = get_db()
    task = request.json
    Task = Query()
    if task is not None and task['title']:
        result = db.search(Task.id == task_id)
        if len(result) >= 1:
            need_updated = result[0]
            need_updated['title'] = task['title']
            db.update(need_updated, Task.id == task_id)
            return jsonify({'id': task_id})
        else:
            return jsonify({'msg': 'NOT FOUND'}), 404
    else:
        return jsonify({'msg': 'title is required'}), 422

@app.route("/api/v1/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    db = get_db()
    Task = Query()
    result = db.search(Task.id == task_id)
    if len(result) >= 1:
        opposite = not result[0]['done']
        db.update({'done': opposite}, Task.id == task_id)
        return jsonify({'id': task_id, 'done': opposite})
    else:
        return jsonify({'msg': 'NOT FOUND'}), 404


@app.route("/api/v1/tasks/<task_id>", methods=["DELETE"])
def remove_task(task_id):
    db = get_db()
    Task = Query()
    result = db.search(Task.id == task_id)
    if len(result) >= 1:
        db.remove(Task.id == task_id)
        return jsonify({'id': task_id})
    else:
        return jsonify({'msg': 'NOT FOUND'}), 404

if __name__ == '__main__':
    app.run(port='12306', debug=True)
