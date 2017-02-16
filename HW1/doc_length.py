from elasticsearch import Elasticsearch
import pickle
import glob

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh("hw1_dataset")

path = "E:/IR/Data/AP_DATA/ap89_collection/*"
files = glob.glob(path)
no_of_files = 0
doc_length_dic = {}

for file in files:
    no_of_files += 1
    print(no_of_files)
    open_file = open(file, "r")
    data = open_file.readlines()
    document_no = None
    for line in data:
        line = line.strip("\n")
        if line.startswith("<DOCNO>"):
            document_no = line.split()[1]
            result = es.search(index="hw1_dataset", doc_type='document', body={"query": {
                "function_score": {
                    "filter": {
                        "query": {
                            "match": {
                                "docno": document_no
                            }
                        }
                    },
                    "functions": [
                        {"script_score": {
                            "script": "getdoclength"
                        }}
                    ],
                    "boost_mode": "replace"
                }
            }
            }, size=500)

            doc_length_dic[document_no] = result['hits']['hits'][0]['_score']

output = open('doc_length.pkl', 'wb')
pickle.dump(doc_length_dic, output)
