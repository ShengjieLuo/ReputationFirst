gsutil rm -r gs://group688/688v1
gcloud dataproc jobs submit pyspark \
--cluster spark688 \
--region us-east1 \
etl.py
