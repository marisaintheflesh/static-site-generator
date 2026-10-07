import os
import sys
import shutil
import json

from pathlib import Path
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader
from markdown2 import Markdown
import toml

from siteConfig import config, podcastconfig

dtfmt = {"html": "%a, %b %d, %Y (%Y-%m-%d) %I:%M:%S %p UTC", "sitemapxml": "%Y-%m-%d", "rss": "%a, %d %b %Y %H:%M:%S GMT", "atom": "%Y-%m-%dT%H:%M:%SZ"}
templates = {"html": "template.html.tpl", "sitemapxml": "sitemap.xml.tpl", "sitemaptxt": "sitemap.txt.tpl", "rss": "template.rss.tpl", "atom": "template.atom.tpl", "podcastrss": "podcast.rss.tpl"}
ts = {}
dirs = {"root": Path(__file__).resolve().parent, "static": "static", "output": "__site", "templates": "templates", "pages": "pages", "posts": "posts", "podcasts": "podcasts", "static_podcasts": "static_podcasts"}

env = None
markdown = Markdown()
now = int(datetime.now(timezone.utc).timestamp())


def format_datetime(ts, format_string):
    date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime(format_string)
    return date


def get_file_contents(filename):
    with open(filename, "r", encoding="utf-8") as file:
        contents = file.read()
    return contents


def write_file_contents(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    return True


def ts2str(timestamp=datetime.now(timezone.utc).timestamp(), format=dtfmt["html"]):
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(format)
    return date


def mksite():
    pages_files = [str(file) for file in Path(dirs["root"] / dirs["pages"]).glob("*.md") if file.is_file()]
    posts_files = [str(file) for file in Path(dirs["root"] / dirs["posts"]).glob("*.md") if file.is_file()]

    podcasts_files = [str(file) for file in Path(dirs["root"] / dirs["podcasts"]).glob("*.toml") if file.is_file()]

    pages = []
    posts = []
    podcasts = []

    for page in pages_files:
        p = get_file_contents(page).split("---", 2)
        tomll = toml.loads(p[0])
        content = markdown.convert(p[1])
        base = Path(page).stem
        lastmod = tomll["lastmod"]
        created = tomll["created"]
        title = tomll["title"]
        pages.append({"base": base, "lastmod": lastmod, "created": created, "title": title, "content": content})

    for post in posts_files:
        p = get_file_contents(post).split("---", 2)
        tomll = toml.loads(p[0])
        content = markdown.convert(p[1])
        base = Path(post).stem
        lastmod = tomll["lastmod"]
        created = tomll["created"]
        title = tomll["title"]
        description = tomll["description"]
        posts.append({"base": base, "lastmod": lastmod, "created": created, "title": title, "content": content, "description": description})

    for podcast in podcasts_files:
        p = get_file_contents(podcast)
        tomll = toml.loads(p)
        title = tomll["title"]
        description = tomll["description"]
        created = tomll["created"]
        lastmod = tomll["lastmod"]
        base = Path(podcast).stem
        size = tomll["size"]
        duration = tomll["duration"]
        explicit = tomll["explicit"]
        episode = tomll["episode"]
        podcasts.append({"base": base, "lastmod": lastmod, "created": created, "title": title, "description": description, "size": size, "duration": duration, "explicit": explicit, "episode": episode})


    os.mkdir(dirs["root"] / dirs["output"] / dirs["pages"])
    os.mkdir(dirs["root"] / dirs["output"] / dirs["posts"])
    os.mkdir(dirs["root"] / dirs["output"] / dirs["podcasts"])

    for page in pages:
        if page["base"] == "index":
            c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=page["title"], content=page["content"], lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"], now=now, type="page")
            write_file_contents(dirs["root"] / dirs["output"] / "index.html", c)
        elif page["base"] == "pages":
            c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=page["title"], content="", lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"],now=now, type="page")
            write_file_contents(dirs["root"] / dirs["output"] / dirs["pages"] / "index.html", c)
        elif page["base"] == "posts":
            c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=page["title"], content="", lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"],now=now,type="page")
            write_file_contents(dirs["root"] / dirs["output"] / dirs["posts"] / "index.html", c)
        elif page["base"] == "podcasts":
            c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=page["title"], content="", lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"], now=now, type="page")
            write_file_contents(dirs["root"] / dirs["output"] / dirs["podcasts"] / "index.html", c)
        else:
            os.mkdir(dirs["root"] / dirs["output"] / dirs["pages"] / page["base"])
            c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=page["title"], content=page["content"], lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"], now=now, type="page")
            write_file_contents(dirs["root"] / dirs["output"] / dirs["pages"] / page["base"] / "index.html", c)

    for post in posts:
        os.mkdir(dirs["root"] / dirs["output"] / dirs["posts"] / post["base"])
        c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=post["title"], content=post["content"], description=post["description"], lastmod=post["lastmod"], created=post["created"], base=post["base"], datasrc=post, fmt=dtfmt["html"], now=now, type="post")
        write_file_contents(dirs["root"] / dirs["output"] / dirs["posts"] / post["base"] / "index.html", c)

    for podcast in podcasts:
        os.mkdir(dirs["root"] / dirs["output"] / dirs["podcasts"] / podcast["base"])
        c = ts["html"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, title=podcast["title"], content=podcast["description"], created=podcast["created"], lastmod=podcast["lastmod"], base=podcast["base"], explicit=podcast["explicit"], episode=podcast["episode"], size=podcast["size"], duration=podcast["duration"], datasrc=podcast, fmt=dtfmt["html"], fmtrss=dtfmt["rss"], now=now, type="podcast")
        write_file_contents(dirs["root"] / dirs["output"] / dirs["podcasts"] / podcast["base"] / "index.html", c)
        if os.path.exists(str(dirs["root"] / dirs["static_podcasts"] / podcast["base"]) + ".mp3"):
            shutil.copy(str(dirs["root"] / dirs["static_podcasts"] / podcast["base"]) + ".mp3", str(dirs["root"] / dirs["output"] / dirs["podcasts"] / podcast["base"] / podcast["base"]) + ".mp3")
        else:
            print(f"WARNING: Could not find {podcast['base']}.mp3! Did you pull the git repo using getPodcasts.sh?")

    # RSS
    c = ts["rss"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, fmt=dtfmt["rss"], now=now)
    write_file_contents(dirs["root"] / dirs["output"] / "feed.rss", c)

    # Atom
    c = ts["atom"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, fmt=dtfmt["atom"], now=now)
    write_file_contents(dirs["root"] / dirs["output"] / "feed.atom", c)
    
    # sitemap.xml
    c = ts["sitemapxml"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, fmt=dtfmt["sitemapxml"], now=now)
    write_file_contents(dirs["root"] / dirs["output"] / "sitemap.xml", c)
    
    # sitemap.txt
    c = ts["sitemaptxt"].render(site=config, podcastconfig=podcastconfig, pages=pages, posts=posts, podcasts=podcasts, fmt=dtfmt["sitemapxml"], now=now)
    write_file_contents(dirs["root"] / dirs["output"] / "sitemap.txt", c)

    # podcasts.rss
    c = ts["podcastrss"].render(site=config, podcastconfig=podcastconfig, podcast=podcastconfig, podcasts=podcasts, fmt=dtfmt["rss"], now=now)
    write_file_contents(dirs["root"] / dirs["output"] / dirs["podcasts"] / "podcasts.rss", c)


def main():
    env = Environment(
        loader=FileSystemLoader(dirs["root"] / dirs["templates"])
    )
    env.filters["datetimeformat"] = format_datetime
    for tplname, tplvalue in templates.items():
        ts[tplname] = env.get_template(tplvalue)
    
    if os.path.exists(dirs["root"] / dirs["output"]):
        shutil.rmtree(dirs["root"] / dirs["output"])
    
    shutil.copytree(dirs["root"] / dirs["static"], dirs["root"] / dirs["output"])

    mksite()

if __name__ == "__main__":
    main()

