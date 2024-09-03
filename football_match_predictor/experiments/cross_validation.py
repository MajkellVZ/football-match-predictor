import logging
import os

import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from football_match_predictor.util.google_cloud_manager import load_data_from_gcs
from football_match_predictor.util.logger import Logger
from football_match_predictor.util.hasher import generate_hash, generate_model_hash
from football_match_predictor.util.neptune_manager import init_neptune
from football_match_predictor.util.parameter_retriever import get_parameters

logger = Logger(name="cross_validation", level=logging.DEBUG)


def load_versioned_data(start_year: int, end_year: int):
	data_hash = generate_hash(start_year, end_year)
	versioned_dir = f'data/{data_hash}/'

	features_blob_name = f'{versioned_dir}features.pickle'
	target_blob_name = f'{versioned_dir}target.pickle'

	X = load_data_from_gcs(features_blob_name)
	y = load_data_from_gcs(target_blob_name)

	return X, y


def main(start_year: int, end_year: int):
	run = init_neptune()

	run['parameters'] = {
		'start_year': start_year,
		'end_year': end_year
	}

	X, y = load_versioned_data(start_year, end_year)

	logger.info("Splitting the data")
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	preprocessor = ColumnTransformer(
		transformers=[
			('num', StandardScaler(), X.columns)
		],
		remainder='passthrough'
	)

	pipeline = Pipeline(steps=[
		('preprocessor', preprocessor),
		('classifier', KNeighborsClassifier())
	])

	param_grid = {
		'classifier__n_neighbors': range(10, 41),
		'classifier__p': [1, 2]
	}

	grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)

	logger.info("Cross validating")
	grid_search.fit(X_train, y_train)

	run['best_params'] = grid_search.best_params_
	run['best_score'] = grid_search.best_score_

	logger.info(f"Best parameters: {grid_search.best_params_}")
	logger.info(f"Best cross-validation accuracy: {grid_search.best_score_}")

	logger.info("Storing model")
	model_hash = generate_model_hash(grid_search.best_params_, start_year, end_year)
	model_path = f'models/model_{model_hash}.pickle'
	os.makedirs(os.path.dirname(model_path), exist_ok=True)
	joblib.dump(grid_search.best_estimator_, model_path)

	test_accuracy = grid_search.score(X_test, y_test)
	logger.info(f"Test accuracy: {test_accuracy}")

	run['test_accuracy'] = test_accuracy

	run.stop()


if __name__ == "__main__":
	start_year, end_year = get_parameters()

	main(start_year, end_year)
