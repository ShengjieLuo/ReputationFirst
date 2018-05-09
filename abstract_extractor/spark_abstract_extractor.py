import time
import json
import datetime
import pyspark

def get_result_list(lines):
    from summa import summarizer
    from summa import keywords
    import nltk
    nltk.download('punkt',download_dir='./nltk_data')
    nltk.data.path.append("./nltk_data")
    result_list = []
    for line in lines:
        json_data = json.loads(line)
        text      = json_data["text"]
        abstract  = summarizer.summarize(text)
        keyword   = keywords.keywords(text, split=True)
        name = json_data['company']
        tags_words = list(map(lambda x: x[1:], json_data['tags']))
        abstract_words = list(map(lambda x: x.lower(), nltk.tokenize.word_tokenize(abstract)))
        title_words = list(map(lambda x: x.lower(), nltk.tokenize.word_tokenize(json_data['title'])))
        if abstract != '' and name not in abstract_words and name not in title_words and name not in tags_words:
            continue
        json_data['abstract'] = abstract
        json_data['keywords'] = keyword
        result_list.append(json.dumps(json_data))
    return result_list

if __name__=="__main__":
    sc = pyspark.SparkContext()
    dataRDD = sc.textFile("gs://group688/688v2.dat",20)
    dataRDD.mapPartitions(get_result_list).saveAsTextFile("gs://group688/688v3")
