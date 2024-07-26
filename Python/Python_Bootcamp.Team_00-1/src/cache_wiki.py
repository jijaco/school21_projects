from bs4 import BeautifulSoup
import requests
import argparse
from urllib.parse import urlparse
import logging
import sys
import json


logger = logging.getLogger("wiki_cache")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(
    prog='cache_wiki',
    description='What the program does',
    epilog='Text at the bottom of help')

parser.add_argument('-p', '--starting_query')
parser.add_argument('-d', '--depth')

args = parser.parse_args()

if args.depth and int(args.depth) < 1:
    print("Argument of depth must be positive")
    exit(1)
elif args.starting_query is None:
    print("No starting point provided")
    exit(1)


def get_html(q, starting_url):
    q = q.replace(" ", "_")
    response = requests.get(
        url=starting_url + q,
    )
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_h1(html):
    patterns = html.find_all("h1")[0]
    for p in patterns:
        return p.get_text().strip()


class GraphWiki:
    depth = 3

    def __init__(self, query, depth=3):
        self.graph = {}
        self.starting_vertice = get_html(query, "https://en.wikipedia.org/wiki/")
        if depth:
            self.depth = int(depth)

    def start_bfs(self):
        url = 'https://en.wikipedia.org/wiki/' + get_h1(self.starting_vertice).replace(" ", "_")
        self.bfs(url, self.depth)

    def bfs(self, url, deep=3):
        soup = get_html(url, "")
        url = urlparse(url)
        key = get_h1(soup)
        if key not in self.graph:
            self.graph[key] = []
        else:
            return

        see_also_sections = []

        if deep == 0:
            return

        see_also_section = soup.find('span', {'id': 'See_also'})
        if see_also_section:
            see_also_links = see_also_section.find_next('ul')
            if see_also_links.has_attr("role") and see_also_links["role"] == "navigation":
                see_also_links = see_also_links.find_next('ul')
            see_also_sections.append(see_also_links)
            if see_also_links.find_next('ul'):
                see_also_sections.append(see_also_links.find_next('ul'))
            for section in see_also_sections:
                if section:
                    links = section.find_all('a')
                    for link in links:
                        final_link = url.scheme + "://" + url.netloc + link['href']
                        if ".wikipedia.org/" in final_link:
                            heading = get_h1(get_html(final_link, ""))
                            if heading in self.graph[key]:
                                return
                            self.graph[key].append(heading)
                            logger.info('New node: ' + str(key) + " - " + str(heading) + " | depth " + str(deep))
                            self.bfs(final_link, deep - 1)


gw = GraphWiki(args.starting_query, args.depth)
gw.start_bfs()

json.dump(gw.graph, open("wiki.json", 'w'))
