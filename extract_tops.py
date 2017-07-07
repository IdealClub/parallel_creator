# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:27:55 2017

Extract top-K sentence pairs with filtering out identical and noisy pairs.

Command-line args: <ranking file> <topK> <corpus-A> <corpus-B> <article nos> [<max-overlap>]
@author: vurga
"""

import sys, string, editdistance, re
from nltk.corpus import stopwords
from langdetect import detect

with open(sys.argv[1], 'r') as source:
    ranks = source.readlines()



def compare_snt(a, b, max_overlap=.65):
    
    try:
        if detect(a) == detect(b):
            return False
    except:
        pass
    
    for ch in a:
        if ch in set(["\\", "=", "+", "/", "}", "_", "→"]):
            return False
        
    for ch in b:
        if ch in set(["\\", "=", "+", "/", "}", "_", "→"]):
            return False
    
    a = re.sub("""(['\-`"])([^ ])""", "\\1 \\2", re.sub("""([^ ])(['\-`"])""", "\\1 \\2", a))
    b = re.sub("""(['\-`"])([^ ])""", "\\1 \\2", re.sub("""([^ ])(['\-`"])""", "\\1 \\2", b))
    
    translator = str.maketrans('', '', string.punctuation+'-'+'–')
    a = a.translate(translator).lower()
    b = b.translate(translator).lower()
      
    a = [w for w in a.split() if w not in stopwords.words() and not w.isnumeric()]
    b = [w for w in b.split() if w not in stopwords.words() and not w.isnumeric()]
    
    #print(a, b)
    
    if (len(a) > 3 and len(b) > 3) and (1 - (editdistance.eval(a, b) / max(len(a), len(b))) < max_overlap):
        print(a, b)
        print(editdistance.eval(a, b) / max(len(a), len(b)))
        return True
    return False
    
    
    
i = 0
r = 0
a_len_dict = dict()
b_len_dict = dict()

a_corp_dict = dict()
b_corp_dict = dict()

while i < int(sys.argv[2]) and r < len(ranks):
    
    rank_line = ranks[r].strip().split()
    split_id = int(rank_line[-1])
    
    article = int(rank_line[0])
    snt_a = int(rank_line[1])
    snt_b = int(rank_line[2])
    
    if split_id not in a_len_dict.keys():
        with open(sys.argv[5]+str(split_id), 'r') as source:
            nos = source.readlines()
        lengths_a = []
        lengths_b = []
        for no in nos:
            lengths_a.append(int(no.strip().split()[0]))
            lengths_b.append(int(no.strip().split()[1]))
        del nos
        a_len_dict[split_id] = lengths_a
        b_len_dict[split_id] = lengths_b
         
        with open(sys.argv[3]+str(split_id), 'r') as source_a, open(sys.argv[4]+str(split_id), 'r') as source_b:
            a_corp_dict[split_id] = source_a.readlines()
            b_corp_dict[split_id] = source_b.readlines()
            
    start_a = sum(a_len_dict[split_id][:article])
    start_b = sum(b_len_dict[split_id][:article])
    
    sentence_a = a_corp_dict[split_id][start_a+snt_a]
    sentence_b = b_corp_dict[split_id][start_b+snt_b]
    
    ## compare
    if compare_snt(sentence_a, sentence_b, float(sys.argv[6])):
        i += 1
        sys.stdout.write(sentence_a+" \n")
        sys.stdout.write(sentence_b+" \n")
        sys.stdout.write("\n")
        
    r += 1
    
            
    
    
    
    


