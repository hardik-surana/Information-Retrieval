from elasticsearch import Elasticsearch
import glob
from urllib2 import Request, urlopen, URLError
from bs4 import BeautifulSoup
import re
from unidecode import unidecode

INDEX = 'hms-index'
TYPE = 'document'
FIELD_NAME = 'DOCNO'

def get_html(url):
    req = Request(url)
    raw_html = ""
    try:
        response = urlopen(req)
    except URLError as e:
        raw_html = ""
    except UnicodeEncodeError as u:
        raw_html = ""
    except UnicodeDecodeError as d:
        raw_html = ""
    else:
        try:
            raw_html = response.read()
        except Exception as ex:
            raw_html = ""

    return raw_html

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
    return unidecode(text)

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)

path = "E:/IR/HW3/data*"
files = glob.glob(path)
file_count = 0
doc_dict = {}
for file in files:
    file_count += 1
    print(file_count)
    openfile = open(file, "r")
    uncompressed_data = openfile.readlines()
    text_data = ""
    terms = set([])
    document_no = None
    text = False
    for line in uncompressed_data:
        line = line.rstrip("\n")
        if line.startswith("</TEXT>"):
            try:
                doc_dict[document_no] = doc_dict[document_no] + text_data
            except KeyError:
                doc_dict[document_no] = text_data
            text_data = ""
            text = False
        elif text:
            text_data = text_data + " " + line
            terms.update(line.split())
        elif line.startswith("<DOCNO>"):
            document_no = line.split()[1]
        elif line.startswith("<TEXT>"):
            text = True
        elif line.startswith("</DOC>"):
            res = es.index(index=INDEX, doc_type=TYPE, id=document_no, body={
                'docno': document_no,
                'html_Source': get_html(document_no),
                'text': get_body(doc_dict[document_no])
            })
            text_data = ""
            # end
