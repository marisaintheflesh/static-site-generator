<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:podcast="https://podcastindex.org/namespace/1.0">
	<channel>
		<title>{{ podcast.title }}: {{ podcast.subtitle }}</title>
		<atom:link href="{{ site.baseURL }}/podcasts/podcasts.rss" type="application/rss+xml" rel="self" />
		<link>{{ site.baseURL }}/podcasts/podcasts.rss</link>
		<language>{{ podcast.language | default('en-ca') }}</language>
		<copyright>(c) {{ site.author }}</copyright>
		<description>{{ podcast.description }}</description>
    
		<itunes:author>{{ site.author }}</itunes:author>
		<itunes:subtitle>{{ podcast.description }}</itunes:subtitle>
		<itunes:summary>{{ podcast.description }}</itunes:summary>
		<itunes:explicit>{{ podcast.explicit | default('false') }}</itunes:explicit>
		<itunes:image href="{{ site.baseURL }}/icon.png" />
		<itunes:category text="{{ podcast.category }}" />
		
		<itunes:owner>
			<itunes:name>{{ site.author }}</itunes:name>
			<itunes:email>{{ podcast.email }}</itunes:email>
    		</itunes:owner>
		<podcast:guid>e6cbd7e1-7e84-4311-b54b-ec6bca6da8ad</podcast:guid>
		<podcast:locked owner="noreply@1r1s.gg">yes</podcast:locked>

{% for p in podcasts %}
		<item>
			<title>{{ p.title }}</title>
			<description>{{ p.description }}</description>
			<pubDate>{{ p.created|datetimeformat(fmt) }}</pubDate>
			<link>{{ site.baseURL }}/podcasts/{{ p.base }}/</link>
			<guid isPermaLink="false">{{ p.base }}/</guid>
				
			<enclosure url="{{ site.baseURL }}/podcasts/{{ p.base }}/{{ p.base }}.mp3" length="{{ p.length }}" type="audio/mpeg" />
			<itunes:author>{{ site.author }}</itunes:author>
			<itunes:summary>{{ p.description }}</itunes:summary>
			<itunes:image href="{{ site.baseURL }}/icon.png" />
			<itunes:duration>{{ p.duration }}</itunes:duration>
			<itunes:explicit>{{ p.explicit | default('false') }}</itunes:explicit>
			<itunes:episode>{{ p.episode }}</itunes:episode>
		</item>
{% endfor %}

	</channel>
</rss>
