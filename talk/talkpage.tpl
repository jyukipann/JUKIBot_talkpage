% from bottle import route, run, template, static_file, request
% from JUKIBot_text.markovGen.generateText import *
% import sqlite3
% import random
% from talk.db import *
<html>
	<head>
		<title>ほぼじゅき</title>
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
		<style>
			body{
				text-align: center;
				background: #bbbbbb;
				-webkit-text-size-adjust: 100%;
			}
			div#center {
				width: 450px;
				height: 800px;
				text-align: left;
				
				margin: auto;
			}
			
			/*/////////////////////////////////////////////////
			//LINE風チャット画面(会話方式)を記事に表示する方法
			/////////////////////////////////////////////////*/
			.line__container {
				padding:0;
				background: #7494c0;
				overflow: hidden;
				max-width: 500px;
				margin: 20px auto;
				font-size: 80%;
				border: 4px solid #333333;
				border-radius: 10px;
			}

			/* タイトル部分 */
				.line__container .line__title {
				background: #273246;
				padding: 10px;
				text-align: center;
				font-size: 150%;
				color: #ffffff;
			}

			/* 会話部分 */
				.line__container .line__contents {
				padding: 10px;
				overflow: hidden;
				line-height: 135%;
			}

			.line__container .scroll {
				height: 700px;
				overflow-y: scroll;
			}

			/* スタンプ画像最大幅 */
			.line__container .stamp img {
			max-width:150px;
			}

			/* 相手の会話 */
			.line__container .line__left {
				width: 100%;
				position: relative;
				display: block;
				margin-bottom: 5px;
				max-width: 80%;
				clear: both;
				text-align: left;
			}

			/* アイコン画像 */
			.line__container .line__left figure {
				width: 50px;
				position: absolute;
				top: 15px;
				left: 0;
				padding: 0;
				margin: 0;

			}

			/* 正方形を用意 */
			.line__container .line__left figure img{
				border-radius: 50%;
				width: 50px;
				height: 50px;
			}

			.line__container .line__left .line__left-text {
				margin-left: 70px;
			}

			.line__container .line__left .line__left-text .name {
				font-size: 80%;
				color: #ffffff;
			}

			/* コメントエリア */
			.line__container .line__left .text {
				margin: 0;
				position: relative;
				padding: 10px;
				border-radius: 20px;
				background-color: #ffffff;
			}

			/* 吹き出し */
			.line__container .line__left .text::after {
				content: '';
				position: absolute;
				display: block;
				width: 0;
				height: 0;
				left: -10px;
				top: 10px;
				border-right: 20px solid #ffffff;
				border-top: 10px solid transparent;
				border-bottom: 10px solid transparent;
			}

			/* 自分の会話 */
			.line__container .line__right {
				position: relative;
				display: block;
				margin: 5px 0;
				max-width: 75%;
				float: right;
				margin-right: 15px;
				clear: both;
				text-align: left;
			}

			/* コメントエリア */
			.line__container .line__right .text {
				padding: 10px;
				border-radius: 20px;
				background-color: #8de055;
				margin: 0;
				margin-left: 80px;
			}

			/* 吹き出し */
			.line__container .line__right .text::after {
				content: '';
				position: absolute;
				display: block;
				width: 0;
				height: 0;
				right: -10px;
				top: 10px;
				border-left: 20px solid #8de055;
				border-top: 10px solid transparent;
				border-bottom: 10px solid transparent;
			}

			/* 自分がスタンプを送る時 */
				.line__container .line__right .stamp {
				position: relative;
				margin-left: 80px;
			}

			/* 既読エリア */
			.line__container .line__right .date {
				content: '';
				position: absolute;
				display: block;
				width: 100px;
				text-align: right;
				left: -30px;
				bottom: 0px;
				font-size: 80%;
				color: #ffffff;
			}

			.message_input{
				width: 87%;
			}

			.send_button{
				width: 10%;
				background-color:#5785e3;
			}
		</style>
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
					
						for mr in reversed(list(talk.get_latest(10))):
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