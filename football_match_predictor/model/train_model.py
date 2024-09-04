import logging
import os
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from football_match_predictor.util.google_cloud_manager import load_data_from_gcs, upload_to_gcs
from football_match_predictor.util.logger import Logger
from football_match_predictor.util.hasher import generate_hash
from football_match_predictor.util.neptune_manager import init_project

logger = Logger(name="model_trainer", level=logging.DEBUG)
environment = os.getenv('ENVIRONMENT')


def load_versioned_data(start_year: int, end_year: int):
	data_hash = generate_hash(start_year, end_year)
	versioned_dir = f'data/{data_hash}/'

	features_blob_name = f'{versioned_dir}features.pickle'
	target_blob_name = f'{versioned_dir}target.pickle'

	X = load_data_from_gcs(features_blob_name)
	y = load_data_from_gcs(target_blob_name).ravel()

	return X, y


def main():
	try:
		project = init_project()
		logger.info("Project initialized successfully")
	except Exception as e:
		logger.error(f"Error initializing project: {e}")
		return

	try:
		runs_df = project.fetch_runs_table(sort_by='test_accuracy').to_pandas()
		logger.info("Fetched runs table successfully")
	except Exception as e:
		logger.error(f"Error fetching runs table: {e}")
		return

	best_run_parameters = (runs_df.loc[:, [
		                                     'sys/creation_time',
		                                     'best_params/classifier__n_neighbors',
		                                     'best_params/classifier__p',
		                                     'parameters/start_year',
		                                     'parameters/end_year'
	                                     ]].sort_values('sys/creation_time', ascending=False)
	                       .head(1))

	start_year = best_run_parameters['parameters/start_year'].values[0]
	end_year = best_run_parameters['parameters/end_year'].values[0]
	n_neighbors = best_run_parameters['best_params/classifier__n_neighbors'].values[0]
	p = best_run_parameters['best_params/classifier__p'].values[0]

	logger.info("Loading the data")
	X, y = load_versioned_data(start_year, end_year)

	preprocessor = ColumnTransformer(
		transformers=[
			('num', StandardScaler(), X.columns)
		],
		remainder='passthrough'
	)

	model = Pipeline(steps=[
		('preprocessor', preprocessor),
		('classifier', KNeighborsClassifier(n_neighbors=n_neighbors, p=p))
	])

	logger.info("Fitting the model")
	model.fit(X, y)

	logger.info("Storing model")
	model_path = 'models/model.pickle'
	if environment == 'production':
		with open(f'/gcs/football-results/{model_path}', 'wb') as f:
			pickle.dump(model, f)
	else:
		with open(model_path, 'wb') as f:
			pickle.dump(model, f)
		upload_to_gcs(model_path, model_path)


if __name__ == "__main__":
	main()
