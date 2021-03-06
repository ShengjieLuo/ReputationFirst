# coding: utf-8
import time
import json
from summa import summarizer
from summa import keywords
import nltk
import datetime


def get_abstract_keywords(text):
    return summarizer.summarize(text), keywords.keywords(text, split=True)


def get_result_list(file, num):
    line_count = 0
    abandon_count = 0
    result_list = []
    with open(file, 'r') as raw_data:
        while line_count != num:
            if line_count % 100 == 0:
                print(line_count, datetime.datetime.now())
            line_count += 1
            json_data = json.loads(raw_data.readline())
            abstract, keyword = get_abstract_keywords(json_data['text'])
            name = json_data['company']
            tags_words = list(map(lambda x: x[1:], json_data['tags']))
            abstract_words = list(
                map(lambda x: x.lower(),
                    nltk.tokenize.word_tokenize(abstract)))
            title_words = list(
                map(lambda x: x.lower(),
                    nltk.tokenize.word_tokenize(json_data['title'])))
            if abstract != '' and name not in abstract_words and name not in title_words and name not in tags_words:
                abandon_count += 1
                print(json_data['title'])
                print(abandon_count)
                continue
            json_data['abstract'] = abstract
            json_data['keywords'] = keyword
            result_list.append(json.dumps(json_data))
    return result_list


def get_demo(file, number_of_demo):
    data = get_result_list(file, number_of_demo)
    with open('data_output_sample.dat', 'w') as d:
        for j in data:
            d.write(j + '\n')
