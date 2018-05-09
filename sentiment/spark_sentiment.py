import time
import json
import datetime
import pyspark

def get_result_list(line):
    data    = json.loads(line)
    company = data["company"]
    score   = data["score"]
    date    = data["date"].split("-")
    date    = int(date[0]) * 365 + int(date[1])*31 + int(date[2])
    result  = [data["date"],score["pos"],score["neg"],score["neu"]]
    return ((company,date),result)

def merge_result(line):
    scores  = line[1]
    pos_score = 0
    neg_score = 0
    neu_score  = 0
    for score in scores:
      pos_score += score[1]
      neg_score += score[2]
      neu_score += score[3]
    pos_score /= len(scores)
    neg_score /= len(scores)
    neu_score /= len(scores)
    return (line[0],line[1][0][0]+","+str(pos_score)+","+str(neg_score)+","+str(neu_score))

if __name__=="__main__":
    sc = pyspark.SparkContext()
    dataRDD = sc.textFile("gs://group688/688v4.dat",20)
    dataRDD.map(get_result_list).filter(lambda x:x[0][0]=="facebook")\
           .groupByKey()\
           .mapValues(list)\
           .map(merge_result)\
           .sortBy(lambda x:x[0])\
           .map(lambda x:x[1])\
           .saveAsTextFile("gs://group688/688v5")
