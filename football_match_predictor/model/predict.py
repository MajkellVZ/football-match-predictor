import logging

import pandas as pd

from football_match_predictor.util.google_cloud_manager import load_data_from_gcs
from football_match_predictor.util.logger import Logger

logger = Logger(name="predictor", level=logging.DEBUG)


class Predictor:
	def __init__(self, model_path: str):
		self.model = load_data_from_gcs(model_path)

	def predict(self, home_team: str, away_team: str, features: pd.DataFrame) -> dict:
		if features.shape[1] != len(self.model.named_steps['preprocessor'].transformers_[0][1].get_feature_names_out()):
			raise ValueError("Feature DataFrame has incorrect number of columns.")

		logger.info(f"Predicting match: {home_team} vs {away_team}")
		predictions = self.model.predict(features)

		results = pd.DataFrame({
			'HomeTeam': home_team,
			'AwayTeam': away_team,
			'FTR': predictions
		})
		target_mapping = {1: 'H',0: 'D',2: 'A'}
		results['FTR'] = results['FTR'].map(target_mapping)

		return results.to_dict()
