from elasticsearch import Elasticsearch
from stemming.porter2 import stem
import pickle

# Connecting to elastic search
es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh("hw1_dataset")

# function to get the list of stop words
def get_stopword_list():
    word_list = []
    stoplist = open('E:/Python Workspace/HW1/stoplist.txt', 'r').readlines()
    for line in stoplist:
        i = 0
        line = line.strip('\n')
        word_list.insert(i, line)
        i = +1
    return word_list

# Running queries
query_file = open('E:/IR/Data/AP_DATA/query_desc.51-100.short.txt', 'r')
total_term_freq = {}

for line in query_file:
    if len(line) > 5:
        data = line.split()
        Q0num = data[0].replace(".", "")
        print("running query no. " + Q0num)
        data.remove(data[0])
        stopwords = get_stopword_list()

        for i in range(len(data)):
            query_word = data[i].lower()
            if ',' in query_word:
                query_word = query_word.replace(",", "")
            if '"' in query_word:
                query_word = query_word.replace('"', "")
            if '.' in query_word:
                query_word = query_word.replace(".", "")
            if '(' in query_word:
                query_word = query_word.replace("(", "")
            if ")" in query_word:
                query_word = query_word.replace(")", "")

            if query_word not in stopwords:
                query_word = stem(query_word)
                result = es.search(index='hw1_dataset', doc_type='document', body={"query": {
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
                }}, size=86000)

                ttfp = 0

                # fetching term frequency
                for hit in result['hits']['hits']:
                    doc_id = hit['_source']['docno']

                    tf = hit['_score']

                    ttfp = ttfp + tf

                if query_word not in total_term_freq:
                    total_term_freq[query_word] = ttfp
                    print query_word, ttfp

print(total_term_freq)

output = open('total_tf.pkl', 'wb')
pickle.dump(total_term_freq, output)

# end
