from __future__ import division
from elasticsearch import Elasticsearch
import pickle

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh(index="hw7_5")

document_pickle = open("E:/IR/hw7/document_pkl.pkl", 'rb')
document_dict = pickle.load(document_pickle)

spamword_dict = {}
i = 1

spamword_file = open("E:/IR/HW7/spam_words.txt", 'r')
for line in spamword_file.readlines():
    word = line.strip('\n')
    spamword_dict[i] = word
    i += 1

# document_dict = {}
# res = es.search(index='hw7_5', doc_type='document', body={"query": {
#     "function_score": {
#         "query": {
#             "match_all": {
#             }
#         }}}}, size=76000)
# for hit in res['hits']['hits']:
#     docid = hit["_source"]["docno"]
#     label = hit["_source"]["label"]
#     split = hit["_source"]["split"]
#     docid = docid.encode('ascii', 'ignore')
#     label = label.encode('ascii', 'ignore')
#     split = split.encode('ascii', 'ignore')
#     document_dict[docid] = [(label, split)]

matrix_dict = {}

for key in spamword_dict.keys():
    result = es.search(index='hw7_5', doc_type='document', body={"query": {
        "match_phrase": {
            "text": spamword_dict[key]}
    }}, size=76000)
    for hit in result['hits']['hits']:
        docid = hit["_source"]["docno"].encode('ascii', 'ignore')
        score = hit["_score"]
        if not matrix_dict.__contains__(docid):
            matrix_dict[docid] = [(key, score)]
        else:
            matrix_dict[docid].append((key, score))

test_file = open("E:/IR/HW7/test_matrix.txt", 'a')
test_catalog = open("E:/IR/HW7/test_catalog.txt", 'a')
training_file = open("E:/IR/HW7/training_matrix.txt", 'a')
training_catalog = open("E:/IR/HW7/training_catalog.txt", 'a')
# document_pickle = open("E:/IR/HW7/document_pkl.pkl", 'wb')
#
# pickle.dump(document_dict, document_pickle)
document_pickle.close()

test = 1
train = 1
for key in matrix_dict.keys():
    split = document_dict[key][0][1]
    label = document_dict[key][0][0]
    spamlist = matrix_dict[key]
    if split == "train":
        if label == 'spam':
            training_file.write('%d ' % 0)
        else:
            training_file.write('%d ' % 1)
        for spamword in spamlist:
            training_file.write('%s:%s ' % (spamword[0], spamword[1]))
        training_file.write('\n')
        training_catalog.write('%d %s\n' % (train, key))
        train += 1
    else:
        if label == 'spam':
            test_file.write('%d ' % 0)
        else:
            test_file.write('%d ' % 1)
        for spamword in spamlist:
            test_file.write('%s:%s ' % (spamword[0], spamword[1]))
        test_file.write('\n')
        test_catalog.write('%d %s\n' % (test, key))
        test += 1

for key in document_dict.keys():
    if not matrix_dict.__contains__(key):
        split = document_dict[key][0][1]
        label = document_dict[key][0][0]
        if split == "train":
            if label == 'spam':
                training_file.write('%d ' % 0)
            else:
                training_file.write('%d ' % 1)
            training_file.write('\n')
            training_catalog.write('%d %s\n' % (train, key))
            train += 1
        else:
            if label == 'spam':
                test_file.write('%d ' % 0)
            else:
                test_file.write('%d ' % 1)
            test_file.write('\n')
            test_catalog.write('%d %s\n' % (test, key))
            test += 1
test_catalog.close()
test_file.close()
training_catalog.close()
training_file.close()
