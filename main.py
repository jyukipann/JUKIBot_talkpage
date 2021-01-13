from bottle import route, run, template, static_file, request
from JUKIBot_text.markovGen.generateText import *
import os
print("server start")

@route('/')
def index():
	return static_file('index.html', root = '.')

@route('/hello')
def hello():
	return template('Hello {{string}}', string = 'World')

@route('/talk',  method=["GET", "POST"])
def talkpage():
	return template('./talk/talkpage.tpl', request)

#run(host = 'localhost', port = 8080, debug = True, reload = True)
run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug = True, reload = True)