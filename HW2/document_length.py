import pickle
import glob
import re

# Loading document id pickle file to dict
doc_id_pickle_file = open('E:/IR/Results/stemstop/doc_ids.pkl', 'rb')
doc_id_dict = pickle.load(doc_id_pickle_file)
doc_id_pickle_file.close()

dic_doc_len = {}

def get_stopword_list():
    word_list = []
    stoplist = open('E:/IR/Results/stoplist.txt', 'r').readlines()
    for line in stoplist:
        i = 0
        line = line.strip('\n')
        word_list.insert(i, line)
        i = +1
    return word_list

def get_doc_length(total_text, docno):

    global dic_doc_len
    stopwords = get_stopword_list()
    encodedDocno = doc_id_dict[docno]
    print docno
    term_list = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\w]+", total_text.lower())
    len_list = []
    for term in term_list:
        if term not in stopwords:
            len_list.append(term)

    dic_doc_len[encodedDocno] = len(len_list)
    len_list[:] = []


path = 'E:/IR/Data/AP_DATA/ap89_collection/ap*'
files = glob.glob(path)
print(files)
file_count = 0
document_count = 0
file_no = 1
doc_dict = {}
doc_text_dict = {}
for file in files:

    openfile = open(file, "r")
    uncompressed_data = openfile.readlines()
    text_data = ""
    total_text = ""
    term_list = []
    document_no = None
    text = False
    for line in uncompressed_data:
        line = line.rstrip("\n")
        if line.startswith("</TEXT>"):
            total_text = total_text + text_data
            text_data = ""
            text = False
        elif text:
            text_data = text_data + " " + line
        elif line.startswith("<DOCNO>"):
            document_no = line.split()[1]
        elif line.startswith("<TEXT>"):
            text = True
        elif line.startswith("</DOC>"):
            text_data = ""
            if total_text != "":
                get_doc_length(total_text, document_no)
                total_text = ""

doc_len_pkl = open('E:/IR/Results/doc_len.pkl', 'wb')
pickle.dump(dic_doc_len, doc_len_pkl)
doc_len_pkl.close()
