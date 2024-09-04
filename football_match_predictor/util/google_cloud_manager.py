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


def upload_to_gcs(data: pd.DataFrame | pd.Series, source_file_path: str, destination_blob_name: str):
	if environment != 'production':
		with open(source_file_path, 'wb') as f:
			pickle.dump(data, f)
	else:
		pickle_buffer = io.BytesIO()
		data.to_pickle(pickle_buffer)
		pickle_buffer.seek(0)
		client = storage.Client(project=project_id)
		bucket = client.bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		blob.upload_from_file(pickle_buffer, content_type='application/octet-stream')
	logger.info(f"File uploaded to {destination_blob_name}.")


def load_data_from_gcs(blob_name):
	if environment == 'production':
		data = pd.read_pickle(f'/gcs/football-results/{blob_name}')
	else:
		client = storage.Client(project=project_id)
		bucket = client.bucket(bucket_name)
		blob = bucket.blob(blob_name)

		data = blob.download_as_bytes()
		with io.BytesIO(data) as file_obj:
			try:
				data = pickle.load(file_obj)
				print("Data loaded successfully")
			except Exception as e:
				print(f"An error occurred: {e}")

	logger.info(f"Loaded {blob_name}.")

	return data
