from __future__ import division
import pickle
from stemming.porter2 import stem
import math

doc_id_file = open('E:/IR/Results/stemstop/doc_ids.pkl', 'rb')
doc_id_dict = pickle.load(doc_id_file)
inv_doc_id_dict = {v: k for k, v in doc_id_dict.items()}
doc_id_file.close()

cat_pkl_file = open('E:/IR/Results/stemstop/c_1.pkl', 'rb')
cat_dict = pickle.load(cat_pkl_file)
cat_pkl_file.close()

index_file = open('E:/IR/Results/stemstop/ii_1.txt', 'r')

doc_len_file = open('E:/IR/Results/doc_len.pkl', 'rb')
dic_doc_len = pickle.load(doc_len_file)
doc_len_file.close()

termid_pkl = open('E:/IR/Results/stemstop/term_ids.pkl', 'rb')
term_id_dict = pickle.load(termid_pkl)
termid_pkl.close()

total_docs = len(dic_doc_len)
total_doc_len = sum(dic_doc_len.values())
avg_doc_length = total_doc_len / total_docs

vocab_size = len(term_id_dict)


def get_stopword_list():
    word_list = []
    stoplist = open('E:/IR/Results/stoplist.txt', 'r').readlines()
    for line in stoplist:
        i = 0
        line = line.strip('\n')
        word_list.insert(i, line)
        i = +1
    return word_list


def scoring_function(term_freq, document_id):
    log_part = (term_freq + 1) / (dic_doc_len[int(document_id)] + vocab_size)
    score = math.log(log_part)
    return score

openfile = open("E:/IR/Data/AP_DATA/query_desc.51-100.short.txt", "r")
# loop for query
for line in openfile:
    if len(line) > 5:
        data = line.split()
        Q0num = (data[0]).replace(".", "")
        print(Q0num)
        data.remove(data[0])
        laplace_dict = {}
        stopwords = get_stopword_list()
        for i in range(len(data)):
            q_word = data[i].lower()
            if ',' in q_word:
                q_word = q_word.replace(",", "")
            if '"' in q_word:
                q_word = q_word.replace('"', "")
            if '.' in q_word:
                q_word = q_word.replace(".", "")
            if '(' in q_word:
                q_word = q_word.replace("(", "")
            if ")" in q_word:
                q_word = q_word.replace(")", "")
            if q_word not in stopwords:
                q_word = stem(q_word)
                if term_id_dict.__contains__(q_word):
                    termid = term_id_dict[q_word]
                    position = cat_dict[termid]
                    index_file.seek(position)
                    line = index_file.readline()
                    docs = line.strip('\n').split("|")[1].split(";")
                    df = len(docs) - 1
                    docs = line.strip('\n').split("|")[1].split(";")
                    docs.remove('')
                    for document in docs:
                        tf_list = document.split(":")[1].split(" ")
                        tf_list.remove('')
                        tf = len(tf_list)
                        docid = document.split(":")[0]
                        doc_name = inv_doc_id_dict[int(docid)]

                        if doc_name not in laplace_dict:
                            laplace_dict[doc_name] = 0


        for i in range(len(data)):
            q_word = data[i].lower()
            if ',' in q_word:
                q_word = q_word.replace(",", "")
            if '"' in q_word:
                q_word = q_word.replace('"', "")
            if '.' in q_word:
                q_word = q_word.replace(".", "")
            if '(' in q_word:
                q_word = q_word.replace("(", "")
            if ")" in q_word:
                q_word = q_word.replace(")", "")
            if q_word not in stopwords:
                q_word = stem(q_word)
                word_doc_dict = {}
                remaning_docs = {}
                if term_id_dict.__contains__(q_word):
                    termid = term_id_dict[q_word]
                    position = cat_dict[termid]
                    index_file.seek(position)
                    line = index_file.readline()
                    docs = line.strip('\n').split("|")[1].split(";")
                    df = len(docs) - 1
                    docs = line.strip('\n').split("|")[1].split(";")
                    docs.remove('')
                    for document in docs:
                        tf_list = document.split(":")[1].split(" ")
                        tf_list.remove('')
                        tf = len(tf_list)
                        docid = document.split(":")[0]
                        doc_name = inv_doc_id_dict[int(docid)]

                        if doc_name in laplace_dict:
                            laplace_dict[doc_name] = laplace_dict[doc_name] + scoring_function(tf, docid)
                            word_doc_dict[doc_name] = 0

                    for key in laplace_dict.keys():
                        if key not in word_doc_dict:
                            remaning_docs[key] = 0

                    for doc_id in remaning_docs:
                        laplace_dict[doc_id] = laplace_dict[doc_id] + scoring_function(0, doc_id_dict[doc_id])

        sorted_laplase_dict = (sorted(laplace_dict.iteritems(), key=lambda x: -x[1])[:1000])

        laplase_file = open('E:/IR/Results/laplase_model(1).txt', 'a')

        for (rank, row) in enumerate(sorted_laplase_dict):
            laplase_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, row[0], (rank + 1), row[1]))