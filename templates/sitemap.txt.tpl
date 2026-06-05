{{ site.baseURL }}
{{ site.baseURL }}/posts/
{{ site.baseURL }}/pages/
{% for page in pages %}
{{ site.baseURL }}/pages/{{ page.base }}/
{% endfor %}
{% for post in posts %}
{{ site.baseURL }}/posts/{{ post.base }}/
{% endfor %}