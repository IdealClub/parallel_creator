# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 09:12:38 2017

Create pseudo sentence pairs from comparable Wikipedia articles.

@author: Adam Varga
"""

import sys
import os

## dictionary mapping language IDs to field numbers in matching IDs file
langmap = {"en":0, "de":1, "es":2, "fr":3}


def read_file(filename):
    """Reads file.
    
    Args:
        filename: path of file
    
    Returns:
        lines of file
    """
    
    with open(filename, 'r') as source:
        return source.readlines()
    
def write_parallel(lang_lines):
    """Creates pseudo-parallel corpora for a given language pair.
    
    Args:
        lang_lines: dictionary with language IDs as keys and parallel article
                    lines as values
    
    """
    
    lang1_lines = []
    lang2_lines = []
    lang1_nos = []
    lang2_nos = []
    
    lang1, lang2 = lang_lines.keys()
    for i, line1 in enumerate(lang_lines[lang1]):
        for j, line2 in enumerate(lang_lines[lang2]):
            lang1_lines.append(line1)
            lang2_lines.append(line2)
            lang1_nos.append(str(i))
            lang2_nos.append(str(j))
            
    with open(lang1+"-"+lang2+"."+lang1, "a+") as target:
        target.write('\n'.join(lang1_lines))
    with open(lang1+"-"+lang2+"."+lang2, "a+") as target:
        target.write('\n'.join(lang2_lines))
    with open(lang1+"-"+lang2+"."+lang1+".no", "a+") as target:
        target.write('\n'.join(lang1_nos))
    with open(lang1+"-"+lang2+"."+lang2+".no", "a+") as target:
        target.write('\n'.join(lang2_nos))    
        
    
def read_parallel(lang1, lang2, ids, art_dir):
    """Reads comparable parallel Wikipedia articles for a given language pair.
    
    Args:
        lang1: ID of source language
        lang2: ID of target language
        ids: lines of the matching IDs file
        art_dir: path of article directories
    
    """
    
    try:
        os.chdir(os.path.abspath(art_dir))
    except:
        sys.stderr.write("Path to article directories does not exist.")
        exit(1)   
        
    with open(lang1+"-"+lang2+"."+lang1, "w"):
        pass
    with open(lang1+"-"+lang2+"."+lang2, "w"):
        pass
    with open(lang1+"-"+lang2+"."+lang1+".no", "w"):
        pass
    with open(lang1+"-"+lang2+"."+lang2+".no", "w"):
        pass
    
    for line in lines:
        ## Get article IDs for language pair
        lang_lines = dict()
        for lang in [lang1, lang2]:
            os.chdir(os.path.abspath(art_dir))
            try:
                field_no = langmap[lang] * 2
            except:
                sys.stderr.write("Unknown language.")
                exit(1)
            id_no = line.strip().split()[field_no]
            try:
                os.chdir(lang+".0/plain/"+lang)
            except:
                sys.stderr.write("Language directory does not exist.")
                exit(1)
            ## Figure out base directory
            os.chdir(str(int(int(id_no)//1e+5)))
            ## Read corresponding article
            with open(str(id_no)+"."+lang+".txt") as source:
                lang_lines[lang] = source.readlines()
        
        ## Write sentence combinations to parallel files
        os.chdir(os.path.abspath(art_dir))
        write_parallel(lang_lines)

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python parallel_creator.py <mathced IDs file> <path to article directories>")
        exit(1)
        
    ## Read file of matching IDs
    try:
        lines = read_file(sys.argv[1])
    except:
        sys.stderr.write("File not found.")
        exit(1)
        
    ## Create pseudo-parallel corpora for de->en, es->en, fr->en
    for lang in ["de", "es", "fr"]:
        read_parallel(lang, "en", lines, sys.argv[2])
        
    
