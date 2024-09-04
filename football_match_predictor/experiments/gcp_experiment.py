import logging
import os

from google.cloud import aiplatform
from football_match_predictor.util.logger import Logger

logger = Logger(name="gcp_model_trainer", level=logging.DEBUG)

environment = os.getenv('ENVIRONMENT')
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET')
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
region = 'europe-west4'


def main():
	try:
		aiplatform.init(
			project=project_id,
			location=region,
			staging_bucket=f'gs://{bucket_name}'
		)

		job = aiplatform.CustomJob(
			display_name='experiment-runner',
			worker_pool_specs=[
				{
					"machine_spec": {
						"machine_type": 'n1-standard-4',
					},
					"replica_count": 1,
					"container_spec": {
						"image_uri": f'{region}-docker.pkg.dev/{project_id}/experiment-repo/experiment_pipeline:latest',
						"env": [
							{"name": "GOOGLE_CLOUD_PROJECT", "value": os.getenv("GOOGLE_CLOUD_PROJECT")},
							{"name": "GOOGLE_CLOUD_BUCKET", "value": os.getenv("GOOGLE_CLOUD_BUCKET")},
							{"name": "NEPTUNE_API_KEY", "value": os.getenv("NEPTUNE_API_KEY")},
						],
					},
				}
			]
		)

		job.run(sync=True)
	except Exception as e:
		logger.error('Setting up gcp job failed')
		raise e


if __name__ == "__main__":
	main()
