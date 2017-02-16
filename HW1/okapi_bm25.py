from elasticsearch import Elasticsearch
from stemming.porter2 import stem
import pickle
import math

# Connecting to elastic search
es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh("hw1_dataset")

# Loading document length pickle file to dict
doc_length_pickle_file = open('E:/Python Workspace/HW1/doc_length.pkl', 'rb')
doc_length_dict = pickle.load(doc_length_pickle_file)
doc_length_pickle_file.close()

# Document constants
no_of_docs = 84678  # obtained from elasticsearch marvel/sense
total_doc_length = sum(doc_length_dict.values())
print(total_doc_length)
avg_doc_length = total_doc_length / no_of_docs
print(avg_doc_length)

# function to calculate Okapi TF
def okapi_bm25(tf, df, doc_id):
    log_part = math.log((0.5 + no_of_docs) / (0.5 + df))
    part_2_numerator = (tf + (1.2 * tf))
    part_2_denominator = (tf + (1.2 * ((1 - 0.75) + (0.75 * (doc_length_dict[doc_id] / avg_doc_length)))))
    part_2 = part_2_numerator / part_2_denominator
    okapi_bm25_score = log_part * part_2
    return okapi_bm25_score


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

for line in query_file:
    if (len(line) > 5):
        data = line.split()
        Q0num = data[0].replace(".", "")
        print("running query no. " + Q0num)
        data.remove(data[0])
        okapi_bm25_dict = {}
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
                print(query_word)
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

                df = result['hits']['total']

                # fetching term frequency
                for hit in result['hits']['hits']:
                    doc_no = hit['_source']['docno']

                    tf = hit['_score']

                    if tf > 0:
                        if doc_no in okapi_bm25_dict:
                            okapi_bm25_dict[doc_no] = okapi_bm25_dict[doc_no] + okapi_bm25(tf, df, doc_no)
                        else:
                            okapi_bm25_dict[doc_no] = okapi_bm25(tf, df, doc_no)

        sorted_okapi_bm25_dict = (sorted(okapi_bm25_dict.iteritems(), key=lambda x: -x[1])[:30])
        output = open('okapi_bm25_dict_pkl.pkl', 'wb')
        pickle.dump(sorted_okapi_bm25_dict, output)

        okapi_bm25_file = open('E:/IR/Results/okapi_bm25_model_30.txt', 'a')

        # Creating score file
        for (rank, row) in enumerate(sorted_okapi_bm25_dict):
            okapi_bm25_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, row[0], (rank + 1), row[1]))

            # end
