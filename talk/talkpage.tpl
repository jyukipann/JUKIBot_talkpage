% from bottle import route, run, template, static_file, request
% from JUKIBot_text.markovGen.generateText import *
% import sqlite3
% import random
% from talk.db import *
<html>
	<head>
		<title>ほぼじゅき</title>
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
		<link rel="stylesheet" type="text/css" href="/style">
		
		<script>
			// 最初に、ビューポートの高さを取得し、0.01を掛けて1%の値を算出して、vh単位の値を取得
			let vh = window.innerHeight * 0.01;
			// カスタム変数--vhの値をドキュメントのルートに設定
			document.documentElement.style.setProperty('--vh', `${vh}px`);
			// resizeイベントの取得
			window.addEventListener('resize', () => {
			// あとは上記と同じスクリプトを実行
			let vh = window.innerHeight * 0.01;
			document.documentElement.style.setProperty('--vh', `${vh}px`);
			});
		</script>
	</head>
	<body>
			<div>
			<%
			try:
				message = request.forms.getunicode('message')
			except:
				message = ""
			end
			reply = ""
			if message != "" and message != None:
				mk = markov("./JUKIBot_text/databases/JUKI.db",N=3)
				reply = mk.generateReply(message)
				if reply == "":
					reply = random.choice(["わからん。","うん。","ふーん。","なにそれ。","笑","わかる"])
				end
			end
			talk = talkDB("./talk.db")
			talk.create()
			if message != None and message != "":
				talk.insert(message,reply)
			end
			%>
			<!-- ▼LINE風 ここから -->
			<div class="line__container">
				<!-- タイトル -->
				<div class="line__title">
				ほぼじゅき
				</div>
				<!-- ▼会話エリア scrollを外すと高さ固定解除 -->
				<div class="line__contents scroll">
					<%
					messages = '''<!-- 自分の吹き出し -->
					<div class="line__right">
						<div class="text">{message}</div>
						<span class="date">既読</span>
					</div>
					<!-- 相手の吹き出し -->
					<div class="line__left">
					<figure>
						<img src="https://lh3.googleusercontent.com/pw/ACtC-3em8eTfUNF4gSy8KnO_bDX_m91dloMnrWHpiOdKpjoFztoCOc2O4rV0I4BZUGqYBppHPqllyBTORSDf3UR-Bn9ipxyb4GvVq-orVTbNSbiCkd-MEfBqi0vK6Wf5fFeVkGz1fb6guyLpne7-WrXsIm5K-g=s1398-no?authuser=0" />
					</figure>
					<div class="line__left-text">
						<div class="name">ほぼじゅき</div>
							<div class="text">{reply}</div>
						</div>
					</div>'''
					out = ""
					
						for mr in reversed(list(talk.get_latest(20))):
							out += messages.format(message=mr[1],reply=mr[2])
						end
					
					%>
					{{!out}}
				</div>
				<!--　▲会話エリア ここまで -->
			<div style="text-align : center ; background : white; padding : 5px;">
			<form id="talk" action="/talk" method="post">
				<input type="text" name="message" class="message_input">
				<input type="submit" value="send" class="send_button">
			</form>
			</div>
			</div>
			<!--　▲LINE風 ここまで -->
			<script type="text/javascript">
				let t = document.querySelector(".line__contents.scroll");
				let s = -1, h = t.clientHeight;
				while(s !== t.scrollTop){ s = t.scrollTop, t.scrollTop = s + h; }
			</script>
			
			<p>
			<a href="/">説明ページ</a><br>
			</p>
			</div>
	</body>
</html>