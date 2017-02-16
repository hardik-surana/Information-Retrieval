from __future__ import division
from elasticsearch import Elasticsearch

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh(index="hms-index")
res = es.search(index='hms-index', doc_type='document', body={"query": {
    "function_score": {
        "query": {
            "match": {
                "text": "world war 2"
            }
        },
        "functions": [
            {
                "script_score": {
                    "lang": "groovy",
                    "script_file": "tf-score",
                    "params": {
                        "term": "world war 2",
                        "field": "text"
                    }
                }
            }
        ],
        "boost_mode": "replace"
    }
}}, size=2000)
i = 1
url_list = []
for hit in res['hits']['hits']:
    doc_no = hit['_source']['docno']
    url_list = url_list + [doc_no]
    i += 1
    if i > 1000:
        break
output_file = open('E:/IR/HW4/okapi_bm25_model.txt', 'ab')
for l in url_list:
    output_file.write('%s\n' % (l))
output_file.close()
