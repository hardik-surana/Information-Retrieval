import os
import glob
import pickle
import re
from stemming.porter2 import stem

index_dict = {}
term_no = 1
termid_dict = {}
docid_dict = {}
docno_counter = 1


def write_index(input_dict):
    output_file = open('E:/IR/Results/stem/ii_1.txt', 'a')
    out_pkl = open("E:/IR/Results/stem/c_1.pkl", 'wb')
    temp_cat = {}
    for key in input_dict.keys():
        temp_cat[key] = output_file.tell()
        output_file.write('%d|%s\n' % (key, input_dict[key]))
    pickle.dump(temp_cat, out_pkl)
    out_pkl.close()
    output_file.close()


def merge_index(file_no):
    print "Merging Indexes"
    cat_file_1 = open("E:/IR/Results/stem/c_1.pkl", 'rb')
    cat_file_2 = open("E:/IR/Results/stem/c_" + str(file_no) + ".pkl", 'rb')
    cat_dict_1 = pickle.load(cat_file_1)
    cat_dict_2 = pickle.load(cat_file_2)
    ii_file_1 = open("E:/IR/Results/stem/ii_1.txt", 'rb')
    ii_file_2 = open("E:/IR/Results/stem/ii_" + str(file_no) + ".txt", 'rb')
    global_index_dict = {}
    for key in cat_dict_2.keys():
        if not cat_dict_1.__contains__(key):
            posn = cat_dict_2[key]
            ii_file_2.seek(posn)
            line = ii_file_2.readline()
            words = line.rstrip('\n').replace("\r", '').split('|')
            global_index_dict[key] = words[1]

        elif cat_dict_1.__contains__(key):
            posn1 = cat_dict_1[key]
            posn2 = cat_dict_2[key]
            ii_file_1.seek(posn1)
            ii_file_2.seek(posn2)
            line1 = ii_file_1.readline()
            word1 = line1.rstrip('\n').replace("\r", '').split('|')
            line2 = ii_file_2.readline()
            word2 = line2.rstrip('\n').replace("\r", '').split('|')
            global_index_dict[key] = word1[1] + word2[1]

    for key in cat_dict_1.keys():
        if not global_index_dict.__contains__(key):
            posn = cat_dict_1[key]
            ii_file_1.seek(posn)
            line = ii_file_1.readline()
            words = line.rstrip('\n').replace("\r", '').split('|')
            global_index_dict[key] = words[1]
    cat_file_1.close()
    cat_file_2.close()
    ii_file_1.close()
    ii_file_2.close()

    os.remove("E:/IR/Results/stem/c_1.pkl")
    os.remove("E:/IR/Results/stem/ii_1.txt")
    os.remove("E:/IR/Results/stem/c_" + str(file_no) + ".pkl")
    os.remove("E:/IR/Results/stem/ii_" + str(file_no) + ".txt")
    write_index(global_index_dict)


def dump_data(fileno):
    global index_dict
    print ("Dumping 1000 docs", fileno)
    str1 = 'E:/IR/Results/stem/ii_' + str(fileno) + ".txt"
    str2 = 'E:/IR/Results/stem/c_' + str(fileno) + ".pkl"
    output_file = open(str1, 'a')
    out_pkl = open(str2, 'wb')
    temp_cataloge = {}
    for key in index_dict.keys():
        temp_dict = index_dict[key]
        temp_cataloge[key] = output_file.tell()
        output_file.write('%s|' % (key))
        for docid in temp_dict.keys():
            temp_list = temp_dict[docid]
            output_file.write('%s:' % (docid))
            for item in temp_list:
                output_file.write(' ')
                output_file.write('%s' % (item))
            output_file.write(';')
        output_file.write('\n')
    pickle.dump(temp_cataloge, out_pkl)
    out_pkl.close()
    output_file.close()
    if file_no > 1:
        merge_index(file_no)
    return


def addnewterm(docid, posn):
    posn_list = {docid: [posn]}
    return posn_list


def addtoexsisting(posn_list, docid, posn):
    if not posn_list.__contains__(docid):
        posn_list[docid] = [posn]
    else:
        posn_list[docid].append(posn)
    return posn_list


def create_index(termid, docid, posn):
    global index_dict
    if not index_dict.__contains__(termid):
        index_dict[termid] = addnewterm(docid, posn)
    else:
        index_dict[termid] = addtoexsisting(index_dict[termid], docid, posn)
    return


def create_dict(total_text, docno):
    global term_no
    global termid_dict
    global docid_dict
    global docno_counter
    posn = 1
    docid_dict[docno] = docno_counter
    term_list = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\w]+", total_text.lower())
    for term in term_list:
        term = stem(term)
        if not termid_dict.__contains__(term):
            termid_dict[term] = term_no
            create_index(term_no, docno_counter, posn)
            term_no += 1
            posn += 1
        else:
            create_index(termid_dict[term], docno_counter, posn)
            posn += 1
    docno_counter += 1
    term_list[:] = []
    return


path = "E:/IR/Data/AP_DATA/ap89_collection/ap*"
files = glob.glob(path)
file_count = 0
document_count = 0
file_no = 1
doc_dict = {}
doc_text_dict = {}
for file in files:
    file_count += 1
    openfile = open(file, "r")
    uncompressed_data = openfile.readlines()
    text_data = ""
    total_text = ""
    term_list = []
    document_no = None
    text = False
    for line in uncompressed_data:
        if document_count == 1000:
            dump_data(file_no)
            file_no += 1
            document_count = 0
            index_dict.clear()

        line = line.rstrip("\n")
        if line.startswith("</TEXT>"):
            total_text = total_text + text_data
            text_data = ""
            text = False
        elif text:
            text_data = text_data + " " + line
        elif line.startswith("<DOCNO>"):

            document_no = line.split()[1]
            document_count += 1
        elif line.startswith("<TEXT>"):
            text = True
        elif line.startswith("</DOC>"):
            text_data = ""
            if total_text != "":
                create_dict(total_text, document_no)
                total_text = ""
dump_data(file_no)

f1 = open('E:/IR/Results/stem/term_ids.txt', 'a')
for key in termid_dict.keys():
    f1.write('%s  %s \n' % (key, termid_dict[key]))
termid_pkl = open("E:/IR/Results/stem/term_ids.pkl", 'wb')
pickle.dump(termid_dict, termid_pkl)
doc_pkl = open("E:/IR/Results/stem/doc_ids.pkl", 'wb')
pickle.dump(docid_dict, doc_pkl)
f1.close()
doc_pkl.close()
