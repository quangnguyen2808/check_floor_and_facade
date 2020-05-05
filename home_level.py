# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from underthesea import sent_tokenize

df = pd.read_csv('one_houses_dna_20_4.csv')
df = df[df['category'] == 'home'][['price', 'acreage', 'title', 'desc']]

df['floor'] = [1]*len(df)
df['facade'] = [1]*len(df)
df['dtsd'] = df['acreage']

set_abbreviate = { 'phòng ngủ': ['pn', 'phn'],
            'phòng khách': ['pk', 'phk'],
            'phòng vệ sinh': ['wc', 'tolet', 'toilet'],
            'hợp đồng': ['hđ', 'hd'],
            'đầy đủ': ['full'],
            'nhỏ': ['mini'],
            'tầm nhìn': ['view'],
            'địa chỉ': ['đc', 'đ/c'],
            'miễn phí': ['free'],
            'vân vân' : ['vv'],
            'liên hệ' : ['lh'],
            'trung tâm thành phố': ['tttp'],
            'yêu cầu': ['order'],
            'công viên': ['cv', 'cvien'],
            ' mặt tiền ' : ['mt'],
            ' dtsd ' : ['diện tích sử dụng'],
            'phường' : [' p ', ' ph '],
            'quận' : [' q ', ' qu '],
            '3' : ['ba'],
            '2' : ['hai'],
            '1' : ['một']
            }

def replace_abbreviate(s):
    for key in set_abbreviate:
        s = re.sub('|'.join(set_abbreviate[key]),' {} '.format(key), s)
    return s

def format_text(text):
    arr = [re.sub('[+|()]', ' ', line.lower()) for line in text.split('\n')]
    arr = [re.sub('[.]', '', line) for line in arr if line != '']
    arr = [replace_abbreviate(line) for line in arr]
    arr = [re.sub('[^0-9A-Za-z ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ/%*-,]', ' ', line) for line in arr]
    arr = [re.sub('m2', ' m2', line) for line in arr]
    arr = [" ".join(line.split()) for line in arr]
    formated_text = " ".join(arr)
    return formated_text

df['processed_desc'] = [format_text(desc) for desc in df['desc']]

#   Count facade
def check_facade(text):
    # Default facade = 1
    facade = 1
    if 'kiệt' in text:
        facade = 0
    elif 'mặt tiền' in text:
        pos = text.find('mặt tiền')
        try:
            # case 'n mặt tiền'
            facade = float(text[pos-2])
        except:
            facade = 1
    return facade

df['facade'] = [check_facade(desc) for desc in df['processed_desc']]

def check_floor(text):
    floor = 1
    pos = text.find('tầng')
    if pos != -1:
        # case '3.5 tầng'
        sequence = text[pos-4:pos].replace(',', '').replace(',', '').strip()
        try:   
            floor = float(sequence)/10 if float(sequence) > 10 else float(sequence)
        except:
            try:
                # case '3 tầng'
                floor = float(sequence[-1])
            except:
                pass
   return floor

df['floor'] = [check_floor(desc) for desc in df['processed_desc']]


