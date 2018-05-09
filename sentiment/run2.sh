gsutil rm -r gs://group688/688v5
gcloud dataproc jobs submit pyspark \
--cluster spark688 \
--region us-east1 \
spark_sentiment.py
