import os
import shutil
import sys
from datetime import datetime, timezone
import markdown2
import htmlmin
import cssmin
#import xmlformatter
from jinja2 import Environment, FileSystemLoader, select_autoescape
import html
import copy
import re
import json

args = sys.argv[1:]


config_file = "siteConfig.json"

templates = "templates/"
html_template = "template.html"
rss_template = "template.rss"
atom_template = "template.atom"
sitemap_template = "template.sitemap.xml"


def load_config():
    with open(config_file, "r") as cfg_file:
        cfg = json.load(cfg_file)
        return cfg


config = load_config()


def minify_html(html_text):
    return htmlmin.minify(html_text, remove_optional_attribute_quotes=False)


def minify_css(css_text):
    return cssmin.cssmin(css_text)


def remove_multiple_newline(text_to_replace):
    return re.sub(r"\n+", "\n", text_to_replace.replace("\r\n", "\n"))


#def minify_xml(xml_text):
#    formatter = xmlformatter.Formatter(indent=0, compress=True, encoding_output='UTF-8')
#    return formatter.format_string(xml_text).decode('utf-8')


def parse_markdown(markdown_text):
    return markdown2.markdown(markdown_text)


def generate_sitemap_xml():
    env = Environment(loader=FileSystemLoader(templates))
    t = env.get_template(sitemap_template)

    site_vars = copy.deepcopy(config["site"])
    page_vars = copy.deepcopy(config["pages"])
    post_vars = copy.deepcopy(config["posts"])
    
    site_vars["buildTime"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"

    for page in page_vars:
        page_vars[page]["basename"] = page
        created = datetime.utcfromtimestamp(int(page_vars[page]["created"]))
        lastmod = datetime.utcfromtimestamp(int(page_vars[page]["lastmod"]))
        page_vars[page]["created"] = created.strftime("%Y-%m-%dT%H:%M:%SZ")
        page_vars[page]['lastmod'] = lastmod.strftime("%Y-%m-%dT%H:%M:%SZ")

    for post in post_vars:
        post_vars[post]["basename"] = post
        created = datetime.utcfromtimestamp(int(post_vars[post]["created"]))
        lastmod = datetime.utcfromtimestamp(int(post_vars[post]["lastmod"]))
        post_vars[post]["created"] = created.strftime("%Y-%m-%dT%H:%M:%SZ")
        post_vars[post]['lastmod'] = lastmod.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open("_site/sitemap.xml", "w") as sm_xml:
        sm_xml.write(remove_multiple_newline(t.render(site=site_vars, pages=page_vars, posts=post_vars)))


def generate_sitemap_txt():
    sitemap = ""
    for page in config["pages"]:
        if page == "index":
            sitemap = sitemap + config["site"]["baseURL"] + "\n"
        else:
            sitemap = sitemap + config["site"]["baseURL"] + page + "\n"

    for post in config["posts"]:
        sitemap = sitemap + config["site"]["baseURL"] + post + "\n"

    with open("_site/sitemap.txt", "w") as sm:
        sm.write(remove_multiple_newline(sitemap.strip()))


def generate_atom():
    env = Environment(loader=FileSystemLoader(templates))
    t = env.get_template(atom_template)

    site_vars = copy.deepcopy(config["site"])
    post_vars = copy.deepcopy(config["posts"])

    site_vars["buildTime"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for post in post_vars:
        post_vars[post]["basename"] = post
        created = datetime.utcfromtimestamp(int(post_vars[post]["created"]))
        lastmod = datetime.utcfromtimestamp(int(post_vars[post]["lastmod"]))
        post_vars[post]["created"] = created.strftime("%Y-%m-%dT%H:%M:%SZ")
        post_vars[post]['lastmod'] = lastmod.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open("_site/feed.atom", "w") as atom:
        atom.write(remove_multiple_newline(t.render(site=site_vars, posts=post_vars)))


def generate_rss():
    env = Environment(loader=FileSystemLoader(templates))
    t = env.get_template(rss_template)

    site_vars = copy.deepcopy(config["site"])
    post_vars = copy.deepcopy(config["posts"])

    site_vars["buildTime"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S") + " GMT"

    for post in post_vars:
        post_vars[post]["basename"] = post
        created = datetime.utcfromtimestamp(int(post_vars[post]["created"]))
        lastmod = datetime.utcfromtimestamp(int(post_vars[post]["lastmod"]))
        post_vars[post]["created"] = created.strftime("%a, %d %b %Y %H:%M:%S") + " GMT"
        post_vars[post]["lastmod"] = lastmod.strftime("%a, %d %b %Y %H:%M:%S") + " GMT"

    with open("_site/feed.rss", "w") as rss:
        rss.write(remove_multiple_newline(t.render(site=site_vars, posts=post_vars)))


def generate_post(basename):
    env = Environment(loader=FileSystemLoader(templates))
    t = env.get_template(html_template)

    md = parse_markdown(open("posts/" + basename + ".md", "r").read())

    site_vars = copy.deepcopy(config["site"])
    posts_vars = copy.deepcopy(config["posts"])
    pages_vars = copy.deepcopy(config["pages"])

    for post in posts_vars:
        posts_vars[post]["basename"] = post

    for page in pages_vars:
        pages_vars[page]["basename"] = page

    post_vars = copy.deepcopy(config["posts"][basename])

    created = datetime.utcfromtimestamp(post_vars["created"])
    lastmod = datetime.utcfromtimestamp(post_vars["lastmod"])
    now_dt = datetime.now(timezone.utc)

    post_vars["content"] = md
    post_vars["created"] = created.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    post_vars["lastmod"] = lastmod.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    post_vars["basename"] = basename

    site_vars["buildTime"] = now_dt.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    site_vars["year"] = now_dt.strftime("%Y")

    return minify_html(t.render(site=site_vars, page=post_vars, posts=posts_vars, pages=pages_vars, type="post"))


def generate_static_page(basename):
    env = Environment(loader=FileSystemLoader(templates))
    t = env.get_template(html_template)

    md = parse_markdown(open("pages/" + basename + ".md", "r").read())

    site_vars = copy.deepcopy(config["site"])
    posts_vars = copy.deepcopy(config["posts"])
    pages_vars = copy.deepcopy(config["pages"])

    for post in posts_vars:
        posts_vars[post]["basename"] = post

    for page in pages_vars:
        pages_vars[page]["basename"] = page

    page_vars = copy.deepcopy(config["pages"][basename])

    created = datetime.utcfromtimestamp(page_vars["created"])
    lastmod = datetime.utcfromtimestamp(page_vars["lastmod"])
    now_dt = datetime.now(tz=timezone.utc)

    page_vars["content"] = md
    page_vars["created"] = created.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    page_vars["lastmod"] = lastmod.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    page_vars["basename"] = basename

    site_vars["buildTime"] = now_dt.strftime("%Y-%m-%d %I:%M:%S%p") + " UTC"
    site_vars["year"] = now_dt.strftime("%Y")

    return minify_html(t.render(site=site_vars, page=page_vars, posts=posts_vars, pages=pages_vars, type="page"))


def main():

    if os.path.isdir('_site'):
        shutil.rmtree('_site')
    shutil.copytree('static', '_site')

    for page in config["pages"]:
        if page == "index":
            open("_site/index.html", "w").write(generate_static_page(page))
        else:
            os.mkdir("_site/" + page + "/")
            open("_site/" + page + "/index.html", "w").write(generate_static_page(page))

    for post in config["posts"]:
        os.mkdir("_site/" + post + "/")
        open("_site/" + post + "/index.html", "w").write(generate_post(post))

    if os.path.exists("_site/css/theme.css"):
        css = open("_site/css/theme.css", "r").read()
        css = minify_css(css)
        open("_site/css/theme.min.css", "w").write(css)

    generate_rss()
    generate_atom()
    generate_sitemap_txt()
    generate_sitemap_xml()

    quit()


if __name__ == '__main__':
    main()
