import robotparser
import urlparse
from urllib2 import Request, urlopen, URLError
import os.path
import re
from unidecode import unidecode
from bs4 import BeautifulSoup
import collections
import time

global_url_list = []
AGENT_NAME = 'PySpider'
i = 1
j = 19
pdf = 'pdf'
ogv = 'ogv'
outlink_file = open('E:/IR/HW3/outlinks', 'ab+')


def load_links():
    global outlink_file
    global global_url_list
    for l in outlink_file.readlines():
        url = l.split('\t')[0]
        if url not in global_url_list:
            global_url_list.append(url)

def dump_data(url, text, title, j):
    str1 = 'E:/IR/HW3/data_' + str(j)
    output_file = open(str1, 'ab')
    output_file.write('<DOC>\n')
    output_file.write('<DOCNO> %s </DOCNO>\n' % (url))
    output_file.write('<HEAD> %s </HEAD>\n' % (title))
    output_file.write('<TEXT>\n%s\n</TEXT>\n' % (text))
    output_file.write('</DOC>\n')
    output_file.close()


def canonicalize_url(url, baseurl="", ident=True):
    if ident:
        url = url.lower()
    parts = urlparse.urlparse(url)

    host = parts.hostname
    if parts.scheme:
        scheme = parts.scheme + "://"
    else:
        scheme = "http://"
    if not host:
        if baseurl:
            url = urlparse.urljoin(baseurl, url)
            return canonicalize_url(url, baseurl, ident)
        host = ""
        scheme = ""
    elif ident:
        if host.startswith("www."):
            host = host[4:]

    path = os.path.normpath(parts.path) if parts.path else ''
    path = path.replace("\\", "/")  # fix for windows
    while "//" in path:
        path = path.replace("//", "/")
    if ident:
        return host + path
    return scheme + host + path


def get_title(html):
    soup = BeautifulSoup(html, from_encoding="utf-8")
    if soup.title:
        return soup.title.string
    return ""


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'img']:
        return False
    elif element.name in ['img']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    return True


def get_body(html):
    soup = BeautifulSoup(html, from_encoding="utf-8")
    texts = soup.findAll(text=True)
    text = " ".join(filter(visible, texts))
    text = re.sub("\s+", " ", text)
    return text


def get_links(html, source):
    soup = BeautifulSoup(html, from_encoding="utf-8")
    return [canonicalize_url(link.get('href'), source, False)
            for link in soup.find_all('a')
            if link.get('href')
            and (":" not in link.get('href') or link.get('href').startswith("http"))
            and link.get('href')[0] != "#"]


url_list = collections.deque()
url_list.append('http://www.ranker.com/list/a-list-of-the-world-war-ii-battles-involving-united-states/reference')
url_list.append('http://en.wikipedia.org/wiki/World_War_II')
url_list.append('http://en.wikipedia.org/wiki/Military_history_of_the_United_States_during_World_War_II')
url_list.append('http://www.history.com/topics/world-war-ii')
url_list.append('http://en.wikipedia.org/wiki/List_of_World_War_II_battles_involving_the_United_States')


def write_outlinks(url, outlinks):
    outlink_file.write('%s\t' % url)
    for l in outlinks:
        outlink_file.write('\t%s' % l)
    outlink_file.write('\n')

load_links()
global_url_list.append('http://en.wikipedia.org/wiki/History_of_U.S._foreign_policy')
while i < 20000:
    global url_list
    links = collections.deque()
    for url in url_list:
        if i < 20000:
            spliturl = urlparse.urlsplit(url)
            split_list = spliturl[1].split('.')
            split_list2 = spliturl[2].split('.')
            if split_list.__contains__('www') or split_list.__contains__('en'):
                if split_list.__contains__('wikidata') or split_list2.__contains__('pdf'):
                    continue
                source = spliturl[0] + "://" + spliturl[1] + "/"
                url = canonicalize_url(url, source, False)
                if not global_url_list.__contains__(url):
                    parser = robotparser.RobotFileParser()
                    parser.set_url(urlparse.urljoin(source, 'robots.txt'))
                    try:
                        parser.read()
                    except Exception as e:
                        continue
                    else:
                        if parser.can_fetch(AGENT_NAME, spliturl[0]):
                            start_time = time.time()
                            req = Request(url)
                            try:
                                response = urlopen(req)
                            except URLError as e:
                                continue
                            except UnicodeEncodeError as uni:
                                continue
                            except UnicodeDecodeError as udi:
                                continue
                            else:
                                print str(i) + ' : ' + url
                                outlinks = []
                                try:
                                    raw_html = response.read()
                                except Exception as e:
                                    continue
                                try:
                                    title = get_title(raw_html).encode('utf-8')
                                except TypeError as ty:
                                    title = 'No Title'
                                except AttributeError as at:
                                    title = 'No Title'
                                body = unidecode(get_body(raw_html))
                                outlinks = get_links(raw_html, source)
                                for li in outlinks:
                                    if li not in links:
                                        links.append(li)
                                global_url_list.append(url)
                                try:
                                    write_outlinks(url, outlinks)
                                except UnicodeEncodeError as u :
                                    continue
                                if i % 1000 == 0:
                                    j += 1
                                i += 1
                                dump_data(url, body, title, j)
    url_list.clear()
    url_list = links

outlink_file.close()