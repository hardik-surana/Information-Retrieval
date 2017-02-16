from elasticsearch import Elasticsearch
import glob

INDEX = 'hw1_dataset'
TYPE = 'document'
FIELD_NAME = 'DOCNO'

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)

path = "E:/IR/Data/AP_DATA/ap89_collection/*"
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
                'text': doc_dict[document_no]
            })
            text_data = ""
            # end
