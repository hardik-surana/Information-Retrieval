import glob
import re
import os
import random
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup

INDEX = 'hw7_5'
TYPE = 'document'
ham_dict = {}

ham_file = open('E:/IR/Data/trec07p/full/index', 'r')
for each in ham_file.readlines():
    st = each.strip('\n').split(' ')
    val = st[0]
    doc_no_list = st[1].split('/')
    doc_no = doc_no_list[2]
    if not ham_dict.__contains__(doc_no):
        ham_dict[doc_no] = val


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'img']:
        return False
    elif element.name in ['img']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    return True


def clean_html(text_list):
    for ln in text_list:
        if ln.startswith("Lines"):
            ind = text_list.index(ln)
            continue
        elif ln.startswith("Content-Transfer-Encoding"):
            ind = text_list.index(ln)
        else:
            ind = 2
    text_list = text_list[ind:]
    html = " ".join(text_list)

    try:
        soup = BeautifulSoup(html, "html5lib")
        texts = soup.findAll(text=True)
        text = " ".join(filter(visible, texts))
        text = re.sub("\s+", " ", text)
    except:
        text = "No Text Found"
    return text


def clean_text(text_list):
    for ln in text_list:
        if ln.startswith("Lines"):
            ind = text_list.index(ln)
            continue
        elif ln.startswith("Content-Transfer-Encoding"):
            ind = text_list.index(ln)
        else:
            ind = 2
    text_list = text_list[ind:]
    text = " ".join(text_list)

    return text


es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)

path = "E:/IR/Data/trec07p/data/*"
# path = "E:/IR/Data/mock/*"
files = glob.glob(path)
file_count = 0
doc_dict = {}

for file in files:
    try:
        file_count += 1
        i = 0
        test = 1
        train = 1
        uncompressed_data = []
        x = random.randint(0, 1)
        if x == 0 and test < 15085:
            split = 'test'
            test += 1
        elif x == 1 and train < 60336:
            split = 'train'
            train += 1
        elif x == 0 and test == 15084:
            split = 'train'
            train += 1
        elif x == 1 and train == 60335:
            split = 'test'
            test += 1
        document_no = os.path.basename(file)
        labl = ham_dict[document_no]
        openfile = open(file, "r")
        raw_data = openfile.readlines()
        unclean_data = [x for x in raw_data if x != '\n']
        for every in unclean_data:
            ln = every.rstrip("\n").strip("\t")
            uncompressed_data.append(ln)
        text_data = ""
        text_list = []
        for line in uncompressed_data:
            i += 1
            text_list = uncompressed_data[i:]
            if line.startswith("Content-Type"):
                compare = line.split(" ")
                if compare[1] == "text/html;":
                    text_data = clean_html(text_list)
                    # print text_data
                elif compare[1] == "text/plain;":
                    text_data = clean_text(text_list)
                    # print text_data

        res = es.index(index=INDEX, doc_type=TYPE, id=document_no, body={
            'docno': str(document_no),
            'text': text_data,
            'label': str(labl),
            'split': split
        })
    except:
        continue
    print str(file_count) + " : " + document_no + " | " + split + " | " + labl
