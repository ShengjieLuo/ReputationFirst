import time
import json
import datetime
import pyspark

def get_result_list(lines):
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk.download('punkt',download_dir='./nltk_data')
    nltk.download('vader_lexicon',download_dir='./nltk_data')
    nltk.data.path.append("./nltk_data")
    sia = SentimentIntensityAnalyzer()
    result_list = []
    for line in lines:
        json_data = json.loads(line)
        
        #mode1: major-abstract
        if len(json_data["abstract"])>0:
            score = sia.polarity_scores(json_data["abstract"])
        else:
            score = sia.polarity_scores(json_data["text"])
        json_data["score_abstract"] = score
        
        #mode2: text-based
        score2 = sia.polarity_scores(json_data["text"])
        json_data["score_text"] = score2

        #mode3: sentence-based
        scores = []
        sents  = nltk.sent_tokenize(json_data["text"].lower())
        name   = json_data["company"]
        for sent in sents:
            if name in sent:
                scores.append(sia.polarity_scores(sent))
        try:
            pos_score = 0
            neg_score = 0
            neu_score = 0
            for score in scores:
                pos_score += score["pos"]
                neg_score += score["neg"]
                neu_score += score["neu"]
            pos_score /= len(scores)
            neg_score /= len(scores)
            neu_score /= len(scores)
            json_data["score_sentence"] = {"pos":pos_score,"neg":neg_score,"neu":neu_score}
        except:
            json_data["score_sentence"] = score2

        result_list.append(json.dumps(json_data))
    return result_list

if __name__=="__main__":
    sc = pyspark.SparkContext()
    dataRDD = sc.textFile("gs://group688/688v3/*")
    dataRDD.mapPartitions(get_result_list).saveAsTextFile("gs://group688/688v4")
