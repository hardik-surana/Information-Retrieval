from __future__ import division
from elasticsearch import Elasticsearch

query_file = open('E:/IR/HW5/query.txt', 'r')
es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh(index="hms-index")

for line in query_file:
    if (len(line) > 1):
        data = line.split()
        Q0num = data[0].replace(".", "")
        print("running query no. " + Q0num)
        data.remove(data[0])
        rank_dict = {}
        query_word = ' '.join(data).lower()
        print query_word
        res = es.search(index='hms-index', doc_type='document', body={"query": {
            "function_score": {
                "query": {
                    "match": {
                        "text": query_word
                    }
                },
                "functions": [
                    {
                        "script_score": {
                            "lang": "groovy",
                            "script_file": "tf-score",
                            "params": {
                                "term": query_word,
                                "field": "text"
                            }
                        }
                    }
                ],
                "boost_mode": "replace"
            }
        }}, size=200)
        i = 1
        for hit in res['hits']['hits']:
            doc_no = hit['_source']['docno']
            tf = hit['_score']

            if doc_no in rank_dict:
                rank_dict[doc_no] = rank_dict[doc_no] + tf
            else:
                rank_dict[doc_no] = tf

        sorted_rank_dict = (sorted(rank_dict.iteritems(), key=lambda x: -x[1])[:200])

        okapi_file = open('E:/IR/HW5/Rank_list.txt', 'a')

        # Creating score file
        for (rank, row) in enumerate(sorted_rank_dict):
            okapi_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, row[0], (rank + 1), (rank + 1)))

            #
            #     i += 1
            #     if i > 1000:
            #         break
            # output_file = open('E:/IR/HW5/Rank_list.txt', 'ab')
            # for l in url_list:
            #     output_file.write('%s\n' % (l))
            # output_file.close()
