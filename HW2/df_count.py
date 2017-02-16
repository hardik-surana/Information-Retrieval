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
# print vocab_size


def get_stopword_list():
    word_list = []
    stoplist = open('E:/IR/Results/stoplist.txt', 'r').readlines()
    for line in stoplist:
        i = 0
        line = line.strip('\n')
        word_list.insert(i, line)
        i = +1
    return word_list


stopwords = get_stopword_list()
q_word = stem('take')
if term_id_dict.__contains__(q_word):
    termid = term_id_dict[q_word]
    position = cat_dict[termid]
    index_file.seek(position)
    line = index_file.readline()
    docs = line.strip('\n').split("|")[1].split(";")
    df = len(docs) - 1
    print df
    docs = line.strip('\n').split("|")[1].split(";")
    docs.remove('')
    for document in docs:
        tf_list = document.split(":")[1].split(" ")
        tf_list.remove('')
        tf = len(tf_list)
        docid = document.split(":")[0]
        doc_name = inv_doc_id_dict[int(docid)]
