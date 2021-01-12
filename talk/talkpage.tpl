% from bottle import route, run, template, static_file, request
% from JUKIBot_text.markovGen.generateText import *
% import sqlite3
<html>
	<body>
		<h2>
			<%
			try:
				message = request.forms.get("message")
			exept:
				message = ""
			end
			reply = ""
			if message != "":
				mk = markov(dbpath,N=3)
				reply = mk.generateReply(message)
			end
			%>
			<p>{{message}}</p>
			<p>{{reply}}</p>
			<form id="talk" action="/talkpage" method="post">
				<input type="text" name="message" size="40">
				<input type="submit" value="send">
			</form>
		</h2>
	</body>
</html>