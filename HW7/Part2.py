from __future__ import division
from elasticsearch import Elasticsearch
import pickle
import operator

es = Elasticsearch("localhost:9200", timeout=600, max_retries=10, revival_delay=0)
es.indices.refresh(index="hw7_5")

test_file = open("E:/IR/HW7/Part2/test_matrix.txt", 'a')
test_catalog = open("E:/IR/HW7/Part2/test_catalog.txt", 'a')
training_file = open("E:/IR/HW7/Part2/training_matrix.txt", 'a')
training_catalog = open("E:/IR/HW7/Part2/training_catalog.txt", 'a')
spamlist_file = open("E:/IR/HW7/Part2/spam_list.txt", 'a')

document_pickle = open("E:/IR/hw7/document_pkl.pkl", 'rb')
document_dict = pickle.load(document_pickle)
document_pickle.close()

spamword_dict = {}
i = 1
test = 1
train = 1

for doc in document_dict.keys():
    temp_dict = {}
    print doc

    split = document_dict[doc][0][1]
    label = document_dict[doc][0][0]

    result = es.search(index='hw7_5', doc_type='document', body={"query": {
        "match": {
            "docno": doc
        }
    }})

    docid = result["hits"]["hits"][00]["_id"]
    docid = int(docid.encode('ascii', 'ignore'))

    res = es.termvector(index='hw7_5', doc_type='document', id=docid, body={
        "fields": ["text"],
        "term_statistics": True
    })

    try:
        for hit in res['term_vectors']['text']['terms']:
            tf = res['term_vectors']['text']['terms'][hit]['term_freq']
            tf = float(tf)
            spamword = hit.encode('ascii', 'ignore')
            if not spamword_dict.__contains__(spamword):
                spamword_dict[spamword] = i
                i += 1
            temp_dict[spamword_dict[spamword]] = tf

    except:
        if split == "train":
            if label == 'spam':
                training_file.write('%d ' % 0)
            else:
                training_file.write('%d ' % 1)
            training_file.write('\n')
            training_catalog.write('%d %s\n' % (train, doc))
            train += 1
        else:
            if label == 'spam':
                test_file.write('%d ' % 0)
            else:
                test_file.write('%d ' % 1)
            test_file.write('\n')
            test_catalog.write('%d %s\n' % (test, doc))
            test += 1
        continue

    sorted_dict = sorted(temp_dict.items(), key=operator.itemgetter(0))

    if split == "train":
        if label == 'spam':
            training_file.write('%d ' % 0)
        else:
            training_file.write('%d ' % 1)
        for pair in sorted_dict:
            training_file.write("%d:%f " % (pair[0], pair[1]))
        training_file.write('\n')
        training_catalog.write('%d %s\n' % (train, doc))
        train += 1

    else:
        if label == 'spam':
            test_file.write('%d ' % 0)
        else:
            test_file.write('%d ' % 1)
        for pair in sorted_dict:
            test_file.write("%d:%f " % (pair[0], pair[1]))
        test_file.write('\n')
        test_catalog.write('%d %s\n' % (test, doc))
        test += 1

for each in spamword_dict.keys():
    spamlist_file.write('%d : %s\n' % (spamword_dict[each], each))

test_catalog.close()
test_file.close()
training_catalog.close()
training_file.close()
spamlist_file.close()
