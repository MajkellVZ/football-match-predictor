import logging

from football_match_predictor.features.data_provider import (load_football_data, preprocess_data,
                                                             define_features_and_target)
from football_match_predictor.util.google_cloud_manager import upload_to_gcs
from football_match_predictor.util.hasher import generate_hash
from football_match_predictor.util.logger import Logger
from football_match_predictor.util.parameter_retriever import get_parameters

logger = Logger(name="feature_pipeline", level=logging.DEBUG)


def main(start_year: int, end_year: int):
	df = load_football_data(start_year, end_year)
	df = preprocess_data(df)
	features, target = define_features_and_target(df, ['B365H', 'B365D', 'B365A'], 'FTR')

	data_hash = generate_hash(start_year, end_year)
	versioned_dir = f'data/{data_hash}/'

	upload_to_gcs(features, f'/gcs/football-results/{versioned_dir}features.pickle',
	              f'{versioned_dir}features.pickle')
	upload_to_gcs(target, f'/gcs/football-results/{versioned_dir}target.pickle',
	              f'{versioned_dir}target.pickle')


if __name__ == "__main__":
	start_year, end_year = get_parameters()

	main(start_year, end_year)
