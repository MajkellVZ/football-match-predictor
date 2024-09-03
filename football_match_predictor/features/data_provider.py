import logging
from typing import List, Tuple
import pandas as pd

from football_match_predictor.util.logger import Logger

logger = Logger(name="data_provider", level=logging.DEBUG)


def load_football_data(start_year: int, end_year: int) -> pd.DataFrame:
	logger.info(f"Loading football data from {start_year} to {end_year}.")
	assert start_year < end_year, "start_year should be less than end_year."
	assert start_year >= 0 and end_year <= 99, "Years should be in two-digit format (e.g., 20 for 2020)."

	year_pairs = [(year, year + 1) for year in range(start_year, end_year)]

	dataframes = []

	for start, end in year_pairs:
		url = f"https://www.football-data.co.uk/mmz4281/{start:02d}{end:02d}/E0.csv"
		logger.info(f"Retrieving data for the season {start:02d}-{end:02d} from {url}.")

		try:
			df = pd.read_csv(url)
			dataframes.append(df)
		except Exception as e:
			logger.error(f"Failed to retrieve data for {start:02d}-{end:02d}: {e}")

	merged_df = pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
	logger.info(
		f"Data loading complete. Merged DataFrame has {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")
	return merged_df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
	columns_to_keep = ['HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A']
	for column in columns_to_keep:
		assert column in df.columns, f"Missing required column: {column}"

	df = df[columns_to_keep].copy()

	target_mapping = {'H': 1, 'D': 0, 'A': 2}
	df['FTR'] = df['FTR'].map(target_mapping)
	df.dropna(inplace=True)

	logger.info("Data preprocessing complete.")
	return df


def define_features_and_target(df: pd.DataFrame, features_columns: List[str], target_column: str) -> Tuple[
	pd.DataFrame, pd.Series]:
	for column in features_columns + [target_column]:
		assert column in df.columns, f"Column {column} is missing in the DataFrame."
	features = df[features_columns]
	target = df[target_column]

	logger.info(f"Features shape: {features.shape}, Target shape: {target.shape}")
	return features, target
