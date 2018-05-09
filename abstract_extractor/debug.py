import time
import json
import datetime
import pyspark

def get_result_list(lines):
    result_list = []
    print "abc"
    return result_list

if __name__=="__main__":
    sc = pyspark.SparkContext()
    dataRDD = sc.textFile("gs://group688/688v2.dat")
    dataRDD.mapPartitions(get_result_list).saveAsTextFile("gs://group688/688v3.dat")
