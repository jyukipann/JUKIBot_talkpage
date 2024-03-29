from bottle import route, run, template, static_file, request
from JUKIBot_text.markovGen.generateText import *
import os
from talk.db import *
print("server start")

@route('/index.html')
@route('/')
def index():
	return static_file('index.html', root = '.')

@route('/hello')
def hello():
	return template('Hello {{string}}', string = 'World')

@route('/talk',  method=["GET", "POST"])
def talkpage():
	mk = markov("./JUKIBot_text/databases/JUKI.db",N=3)
	talk = talkDB("./talk.db")
	talk.create()
	return template('./talk/talkpage.tpl', request, mk=mk, talk=talk)

@route("/style")
def style():
	return static_file('./talk/style.css', root = '.')

#run(host = 'localhost', port = 8080, debug = True, reload = True)
run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug = True, reload = True)