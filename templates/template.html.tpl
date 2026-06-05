<!DOCTYPE html>
<html lang="{{ site.language }}" dir="{{ site.textDirection }}">
	<head>
		<meta charset="{{ site.encoding }}">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>{{ site.title }}: {{ site.description }}</title>
		<link rel="stylesheet" type="text/css" href="/PrettyLittlePrincess.css">
		<link rel="shortcut icon" href="/favicon.ico">
		<link rel="icon" type="image/png" href="/icon.png">
		<script type="text/javascript" src="/bounce-animation.js"></script>
	</head>
	<body>
		<div id="page-wrapper">
			<div id="top"></div>
			<div class="page-segment">
				<a href="#content">Skip to content...</a>
			</div>
			<hr>
			<div class="page-segment">
				<div id="header">
					<div id="header-image">
						<img src="/me.jpg" alt="A joyful, smiling trans woman, with long, brown hair, standing in a snow-covered park on a cold day. There are also several trees, a park bench, and a lake in the background behind her. She is wearing several colorful hats, several colorful scarfs, and eyeglasses with purple frames." title="A joyful, smiling trans woman, with long, brown hair, standing in a snow-covered park on a cold day. There are also several trees, a park bench, and a lake in the background behind her. She is wearing several colorful hats, several colorful scarfs, and eyeglasses with purple frames.">
					</div>
					<div id="header-title">
						{{ site.title }}: {{ site.description }}
					</div>
				</div>
			</div>
			<hr>
			<div class="page-segment">
				<div id="mini-bio">
					<span>| a gay, queer and trans woman | she/her/hers | Miss | heart of gold | beam of sunshine | beacon of joy | Queen of Hearts | Queen of Wishful Thinking | Queen Bitch of the Universe | committer of fashion crimes | FUCK THE SYSTEM + ACAB | smart | kind | brave | strong | somewhere, over the rainbow | nerd | geek | adorkable | chaotic good | chaos incarnate | heck in a handbasket | a pretty little princess | Lil Rainbow | everyone's pal and friend | #justMarisaThings |</span>
				</div>
			</div>
			<hr>
			<div class="page-segment">
				<div id="menu">
					<ul>
						{% for pg in pages %}
						<li>
							{% if pg.base == "index" %}
							<a href="/">{{ pg.title }}</a>
							{% elif pg.base == "pages" %}
							<a href="/pages/">{{ pg.title }}</a>
							{% else %}<a href="/pages/{{ pg.base }}/">{{ pg.title }}</a>
							{% endif %}
						</li>
						{% endfor %}
					</ul>
				</div>
			</div>
			<hr>
			<div class="page-segment">
				<div id="content">
					{% if datasrc.base == "pages" %}
						<h1>{{ datasrc.title }}</h1>
						<ul>
						{% for pg in pages %}
						<li>
							{% if pg.base == "index" %}
							<a href="/">{{ pg.title }}</a>
							{% elif pg.base == "pages" %}
							<a href="/pages/">{{ pg.title }}</a>
							{% else %}
							<a href="/pages/{{ pg.base }}/">{{ pg.title }}</a>
							{% endif %}
						</li>
						{% endfor %}
						</ul>
					{% elif datasrc.base == "posts" %}
						<h1>{{ datasrc.title }}</h1>
						<ul>
						{% for pts in posts %}
						<li>
							{% if pts.base == "posts" %}
							<a href="/posts/">{{ pts.title }}</a>
							{% else %}
							<a href="/posts/{{ pts.base }}/">{{ pts.title }}</a>
							{% endif %}
						</li>
						{% endfor %}
						</ul>
					{% else %}
						<h1>{{ title }}</h1>
						{{ content }}
						<br>---<br>
						Created: {{ created|datetimeformat(fmt) }}<br>
						Last Modified: {{ lastmod|datetimeformat(fmt) }}<br>
					{% endif %}
				</div>
			</div>
			<hr>
			<div class="page-segment">
				<div id="footer">
					<p>Thanks for visiting!<br>
					<br>
					Sincerely, everyone's pal and friend,<br>
					Miss Marisa Marion Mackenzie</p>
					<div id="canvas-wrapper">
						<img src="/m-static.png" alt="*" id="static-logo">
      				</div><br>
					Alternative website link: <a href="{{ site.altlink }}">{{ site.altlink }}</a><br>
					Site last generated on: {{ now|datetimeformat(fmt) }}
				</div>
			</div>
			<hr>
			<div class="page-segment">
				<a href="#top">Return to the top of this page...</a>
			</div>
		</div>
	</body>
</html>