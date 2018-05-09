import pyspark
import json
import nltk
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def _sentiment_analysis(lines,company,source):
  import nltk
  nltk.download('punkt',download_dir='./nltk_data')
  nltk.download('vader_lexicon',download_dir='./nltk_data')
  nltk.data.path.append("./nltk_data")
  for line in lines:
    text = json.loads(line)["text"]
    name = json.loads(line)["company"]
    sents = nltk.sent_tokenize(text)
    for sent in sents:
      if sent.count(name)>=1:
        ana = sent
  results = []
  for datum in lines:

def real_main():
  sc = pyspark.SparkContext()
  dataRDD = sc.textFile("gs://group688/688v2.dat",25)
  dataRDD.mapPartitions(_sentiment_analysis)

if __name__=="__main__":
  real_main()
