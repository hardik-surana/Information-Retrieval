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
print vocab_size


def get_stopword_list():
    word_list = []
    stoplist = open('E:/IR/Results/stoplist.txt', 'r').readlines()
    for line in stoplist:
        i = 0
        line = line.strip('\n')
        word_list.insert(i, line)
        i = +1
    return word_list


def okapi_tf(tf, doc_id):
    wokapi_score = 0
    temp1 = tf + 0.5 + (1.5 * ((1.0 * dic_doc_len[int(doc_id)]) / avg_doc_length))
    wokapi_score = (tf * 1.0) / temp1
    return wokapi_score

def tf_idf(tf, df, doc_id):
    log_value = math.log(total_docs / df)
    okapi_score = okapi_tf(tf, doc_id)
    tf_idf_score = okapi_score * log_value
    return tf_idf_score

def okapi_bm25(tf, df, doc_id):
    log_part = math.log((0.5 + total_docs) / (0.5 + df))
    part_2_numerator = (tf + (1.2 * tf))
    part_2_denominator = (tf + (1.2 * ((1 - 0.25) + (0.25 * (dic_doc_len[int(doc_id)] / avg_doc_length)))))
    part_2 = (part_2_numerator / part_2_denominator)
    okapi_bm25_score = (log_part * part_2)
    return okapi_bm25_score


openfile = open("E:/IR/Data/AP_DATA/query_desc.51-100.short.txt", "r")
# loop for query
for line in openfile:
    if len(line) > 5:
        tf_idf_dict = {}
        okapi_bm25_dict = {}
        data = line.split()
        Q0num = (data[0]).replace(".", "")
        data.remove(data[0])
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

                        if tf_idf_dict.__contains__(doc_name):
                            tf_idf_dict[doc_name] = tf_idf_dict[doc_name] + tf_idf(tf, df, docid)
                        else:
                            tf_idf_dict[doc_name] = tf_idf(tf, df, docid)

                        if okapi_bm25_dict.__contains__(doc_name):
                            okapi_bm25_dict[doc_name] = okapi_bm25_dict[doc_name] + okapi_bm25(tf, df, docid)
                        else:
                            okapi_bm25_dict[doc_name] = okapi_bm25(tf, df, docid)

        sorted_tfidf_dict = (sorted(tf_idf_dict.iteritems(), key=lambda x: -x[1])[:1000])

        sorted_okapi_bm25_dict = (sorted(okapi_bm25_dict.iteritems(), key=lambda x: -x[1])[:1000])

        tf_idf_file = open('E:/IR/Results/tfidf_model.txt', 'a')
        okapi_bm25_file = open('E:/IR/Results/okapi_bm25_model.txt', 'a')

        for (rank, row) in enumerate(sorted_tfidf_dict):
            tf_idf_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, row[0], (rank + 1), row[1]))

        for (rank, row) in enumerate(sorted_okapi_bm25_dict):
            okapi_bm25_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, row[0], (rank + 1), row[1]))
