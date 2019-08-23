from flask import Flask, jsonify, request
import redis, random
app = Flask(__name__)
r = redis.Redis()

# counter
@app.route('/')
def index_page():
    views = r.get("views")
    if views is None:
        views = 0
    else:
        views = int(views) + 1
    r.set("views", views)
    r.expire("views", 10)
    return jsonify(code=100, content='Index Page', views=views)

# add mail to queue
@app.route('/add_mail/<mail>')
def add_mail(mail=None):
    if mail is None:
        return jsonify(code=400, msg='mail is required')
    l = r.lrange("mail_queue", 0, -1)
    r.rpush("mail_queue", mail)
    l = [str(i)+ 'ok' for i in r.lrange("mail_queue", 0, -1)]
    queue = ';'.join(l)
    return jsonify(code=100, queue=queue)

# send mail
@app.route('/send_mail')
def send_mail():
    queue = r.lrange("mail_queue", 0, -1)
    if len(queue) == 0:
        return jsonify(code=400, msg='no mail to send')
    else:
        mail = str(r.lpop("mail_queue"))
        return jsonify(code=100, mail=mail)

@app.route('/vcode/<mobile>')
def send_vcode(mobile=None):
    if mobile is None:
        return jsonify(code=400, msg='mobile is required')
    else:
        if r.exists(mobile):
            return jsonify(code=400, msg='vocde has already sent')
        else:
            code = 9527
            r.setex(mobile, 60, code)
            return jsonify(code=100, vcode=code)



if __name__ == '__main__':
    app.run()
