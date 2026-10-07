<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>{{ site.title }}</title>
    <link>{{ site.baseURL }}</link>
    <description>{{ site.description }}</description>
	<atom:link href="{{ site.baseURL }}/feed.rss" rel="self" type="application/rss+xml" />
    <language>{{ site.language }}</language>
	<pubDate>{{ now|datetimeformat(fmt) }}</pubDate>
	<lastBuildDate>{{ now|datetimeformat(fmt) }}</lastBuildDate>
	
	{% for post in posts %}
	<item>
		<title>{{ post.title }}</title>
		<link>{{ site.baseURL}}/posts/{{ post.base }}/</link>
		<pubDate>{{ post.created|datetimeformat(fmt) }}</pubDate>
		<guid>{{ post.base }}</guid>
		<description>{{ post.description }}</description>
		<author>{{ site.author }}</author>
	</item>
	{% endfor %}
    

</channel>
</rss>
