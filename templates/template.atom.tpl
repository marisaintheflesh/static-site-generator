<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
	<title>{{ site.title}}</title>
	<subtitle>{{ site.description }}</subtitle>
	<link href="{{ site.baseURL }}/feed.atom" rel="self" type="application/atom+xml" />
	<link href="{{ site.baseURL }}" />
	<updated>{{ now|datetimeformat(fmt) }}</updated>
	<author>
		<name>{{ site.author }}</name>
	</author>
	<id>{{ site.baseURL }}/feed.atom</id>
	
	{% for post in posts %}
	<entry>
		<title>{{ post.title }}</title>
		<link href="{{ site.baseURL }}/posts/{{ post.base }}/"/>
		<id>{{ post.base }}</id>
		<updated>{{ post.lastmod|datetimeformat(fmt) }}</updated>
		<summary>{{ post.description }}</summary>
		<content type="html"><![CDATA[{{ post.content }}]]></content>
	</entry>
	{% endfor %}

</feed>