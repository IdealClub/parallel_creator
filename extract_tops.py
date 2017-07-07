# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:27:55 2017

Extract top-K sentence pairs with filtering out identical and noisy pairs.

Command-line args: <ranking file> <topK> <corpus-A> <corpus-B> <article nos> <lang1> <lang2>
@author: vurga
"""

import sys, string, editdistance, re
from nltk.corpus import stopwords

with open(sys.argv[1], 'r') as source:
    ranks = source.readlines()

a_len_dict = dict()
b_len_dict = dict()

a_corp_dict = dict()
b_corp_dict = dict()



def compare_snt(a, b, lan1, lan2):
    
    if re.match("\\\\|=", a) or re.match("\\\\|=", b):
        return False
    
    translator = str.maketrans('', '', string.punctuation)
    a = a.translate(translator).lower()
    b = b.translate(translator).lower()
    
    a = [w for w in a.split() if w not in stopwords.words(lan1)]
    b = [w for w in b.split() if w not in stopwords.words(lan2)]
    
    if editdistance.eval(a, b) > 0:
        return True
    return False
    
    
    
i = 0
r = 0
while i < int(sys.argv[2]) and r < len(ranks):
    
    rank_line = ranks[r].strip().split()
    split_id = rank_line[-1]
    
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
         
        with open(sys.argv[3], 'r') as source_a, open(sys.argv[4], 'r') as source_b:
            a_corp_dict[split_id] = source_a.readlines()
            b_corp_dict[split_id] = source_b.readlines()
            
    start_a = sum(a_len_dict[split_id][:article])
    start_b = sum(b_len_dict[split_id][:article])
    
    snt_a = a_corp_dict[split_id][start_a+snt_a]
    snt_b = b_corp_dict[split_id][start_b+snt_b]
    
    ## compare
    if compare_snt(snt_a, snt_b, sys.argv[6], sys.argv[7]):
        i += 1
        sys.stdout.write(snt_a + '\t' + snt_b)
        
    r += 1
    
            
    
    
    
    


