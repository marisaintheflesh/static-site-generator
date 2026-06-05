import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader
from markdown2 import Markdown
import toml

from siteConfig import config

dtfmt = {"html": "%a, %b %d, %Y (%Y-%m-%d) %I:%M:%S %p UTC", "sitemapxml": "%Y-%m-%d", "rss": "%a, %d %b %Y %H:%M:%S GMT", "atom": "%Y-%m-%dT%H:%M:%SZ"}
templates = {"html": "template.html.tpl", "sitemapxml": "sitemap.xml.tpl", "sitemaptxt": "sitemap.txt.tpl", "rss": "template.rss.tpl", "atom": "template.atom.tpl"}
ts = {}
dirs = {"root": Path(__file__).resolve().parent, "static": "static", "output": "__site", "templates": "templates", "pages": "pages", "posts": "posts"}
env = None
markdown = Markdown()
now = datetime.now(timezone.utc).timestamp()

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
        pages = []
        posts = []
       
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
        
        os.mkdir(dirs["root"] / dirs["output"] / dirs["pages"])
        os.mkdir(dirs["root"] / dirs["output"] / dirs["posts"])
        for page in pages:
            if page["base"] == "index":
                c = ts["html"].render(site=config, pages=pages, posts=posts, title=page["title"], content=page["content"], lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"], now=now)
                write_file_contents(dirs["root"] / dirs["output"] / "index.html", c)
            elif page["base"] == "pages":
                c = ts["html"].render(site=config, pages=pages, posts=posts, title=page["title"], content="", lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"],now=now)
                write_file_contents(dirs["root"] / dirs["output"] / dirs["pages"] / "index.html", c)
            else:
                os.mkdir(dirs["root"] / dirs["output"] / dirs["pages"] / page["base"])
                c = ts["html"].render(site=config, pages=pages, posts=posts, title=page["title"], content=page["content"], lastmod=page["lastmod"], created=page["created"], base=page["base"], datasrc=page, fmt=dtfmt["html"], now=now)
                write_file_contents(dirs["root"] / dirs["output"] / dirs["pages"] / page["base"] / "index.html", c)
                write_file_contents(dirs["root"] / dirs["output"] / dirs["posts"] / "index.html", c)
        for post in posts:
                os.mkdir(dirs["root"] / dirs["output"] / dirs["posts"] / post["base"])
                c = ts["html"].render(site=config, pages=pages, posts=posts, title=post["title"], content=post["content"], lastmod=post["lastmod"], created=post["created"], base=post["base"], datasrc=post, fmt=dtfmt["html"], now=now)
                write_file_contents(dirs["root"] / dirs["output"] / dirs["posts"] / post["base"] / "index.html", c)
           
        # RSS
        c = ts["rss"].render(site=config, pages=pages, posts=posts, fmt=dtfmt["rss"], now=now)
        write_file_contents(dirs["root"] / dirs["output"] / "feed.rss", c)
        
        # Atom
        c = ts["atom"].render(site=config, pages=pages, posts=posts, fmt=dtfmt["atom"], now=now)
        write_file_contents(dirs["root"] / dirs["output"] / "feed.atom", c)
        
        # sitemap.xml
        c = ts["sitemapxml"].render(site=config, pages=pages, posts=posts, fmt=dtfmt["sitemapxml"], now=now)
        write_file_contents(dirs["root"] / dirs["output"] / "sitemap.xml", c)
        
        # sitemap.txt
        c = ts["sitemaptxt"].render(site=config, pages=pages, posts=posts, fmt=dtfmt["sitemapxml"], now=now)
        write_file_contents(dirs["root"] / dirs["output"] / "sitemap.txt", c)


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
    