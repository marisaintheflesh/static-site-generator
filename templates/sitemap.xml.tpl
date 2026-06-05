<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<!-- sitemap.xml last generated on: {{ now|datetimeformat(fmt) }} -->
	{{ pages }}
	{% for page in pages %}
	{% if page.base == "index" %}
	<url>
		<loc>{{ site.baseURL }}/</loc>
		<lastmod>{{ page.lastmod|datetimeformat(fmt) }}</lastmod>
	</url>
	{% elif page.base == "pages" %}
	<url>
		<loc>{{ site.baseURL }}/pages/</loc>
		<lastmod>{{ page.lastmod|datetimeformat(fmt) }}</lastmod>
	</url>
	{% elif page.base == "posts" %}
	<url>
		<loc>{{ site.baseURL }}/posts/</loc>
		<lastmod>{{ page.lastmod|datetimeformat(fmt) }}</lastmod>
	</url>
	{% else %}
	<url>
		<loc>{{ site.baseURL }}/pages/{{ page.base }}/</loc>
		<lastmod>{{ page.lastmod|datetimeformat(fmt) }}</lastmod>
	</url>
	{% endif %}
	{% endfor %}
	
	{% for post in posts %}
	<url>
		<loc>{{ site.baseURL }}/posts/{{ post.base }}/</loc>
		<lastmod>{{ post.lastmod|datetimeformat(fmt) }}</lastmod>
	</url>
	{% endfor %}
</urlset>