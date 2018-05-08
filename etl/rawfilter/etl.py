import pyspark
import json
import nltk
from nltk import word_tokenize

def _init_line(line):
  name = line.lower().split()[0]
  return (name,line.lower().split())

def _init_list(sc):
  results = {}
  companyRDD = sc.textFile("gs://group688/companylist")
  coms = companyRDD.map(_init_line).collect()
  for com in coms:
    for name in com[1]:
      results[name] = com[0]
  return results   

def _data_filter(lines,company,source):
  import nltk
  nltk.download('punkt',download_dir='./nltk_data')
  nltk.data.path.append("./nltk_data")
  results = []
  for datum in lines:
    data    = json.loads(datum)
    authors = data["authors"]
    date    = data["date"]
    text    = data["text"]
    title   = data["title"]
    tokens_text  = word_tokenize(text.lower())
    tokens_title = word_tokenize(title.lower())
    tags = []
    for word in text.lower().split():
      if word[0]=="#":
        tags.append(word.lower())
    #Stat is a dictionary, key is the company name, and value is the attribute
    #attributes: [in_title,title_count,total_count]
    stat  = {}
    for token in tokens_title:
      if token in company:
        if company[token] in stat:
          stat[company[token]][0] = True
          stat[company[token]][1] += 1
        else:
          stat[company[token]] = [True,1,0]
    for token in tokens_text:
      if token in company:
        if company[token] in stat:
          stat[company[token]][2] += 1
        else:
          stat[company[token]] = [False,0,1]
    for name in stat:
      result = {}
      if (source=="wsj"):
        result["date"]      = date[:5] + '0' + date[5:9]
      else:
        result["date"]      = date[:10]
      result["text"]        = text
      result["tokens"]      = tokens_text
      result["company"]     = name
      result["source"]      = source
      result["in_title"]    = stat[name][0]
      result["title_count"] = max(stat[name][1],title.lower().count(name))
      result["total_count"] = max(stat[name][2],text.lower().count(name))
      result["title"]       = title
      result["authors"]     = authors
      result["tags"]        = tags
      results.append((name,json.dumps(result)))
  return results

def real_main():
  sc = pyspark.SparkContext()
  company = _init_list(sc)
  dataRDD1 = sc.textFile("gs://group688/nytimes",5)
  dataRDD1 = dataRDD1.mapPartitions(lambda x:_data_filter(x,company,"nytimes"))
  dataRDD2 = sc.textFile("gs://group688/wsj",10)
  dataRDD2 = dataRDD2.mapPartitions(lambda x:_data_filter(x,company,"wsj"))
  dataRDD3 = sc.textFile("gs://group688/reuters.dat",10)
  dataRDD3 = dataRDD3.mapPartitions(lambda x:_data_filter(x,company,"reuters"))
  dataRDD  = dataRDD3.union(dataRDD2).union(dataRDD1)
  dataRDD.sortByKey().map(lambda x:x[1]).saveAsTextFile("gs://group688/688v1")

if __name__=="__main__":
  real_main()
