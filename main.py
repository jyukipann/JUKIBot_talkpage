from bottle import route, run, template, static_file, request
from JUKIBot_text.markovGen.generateText import *
@route('/')
def index():
	return static_file('index.html', root = '.')

@route('/hello')
def hello():
	return template('Hello {{string}}', string = 'World')

@route('/talkpage', method='post')
def start():
	return template('./talk/talkpage.tpl', request)

run(host = 'localhost', port = 8080, debug = True, reload = True)