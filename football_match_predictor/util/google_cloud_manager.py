import os
import io
import logging
import pickle

import pandas as pd
from google.cloud import storage
from football_match_predictor.util.logger import Logger

logger = Logger(name="gcp_manager", level=logging.DEBUG)


environment = os.getenv('ENVIRONMENT')
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET')
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')


def upload_to_gcs(source_file_path: str, destination_blob_name: str):
	client = storage.Client(project=project_id)
	bucket = client.bucket(bucket_name)
	blob = bucket.blob(destination_blob_name)
	blob.upload_from_filename(source_file_path)
	logger.info(f"File {source_file_path} uploaded to {destination_blob_name}.")


def load_data_from_gcs(blob_name):
	if environment == 'production':
		data = pd.read_pickle(f'/gcs/football-results/{blob_name}')
	else:
		client = storage.Client(project=project_id)
		bucket = client.bucket(bucket_name)
		blob = bucket.blob(blob_name)

		data = blob.download_as_bytes()
		with io.BytesIO(data) as file_obj:
			data = pickle.load(file_obj)

	logger.info(f"Loaded {blob_name}.")

	return data
