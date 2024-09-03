import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from football_match_predictor.features.data_provider import preprocess_data, define_features_and_target


class TestPreprocessData(unittest.TestCase):

	def test_preprocess_data_success(self):
		data = {
			'HomeTeam': ['TeamA', 'TeamB'],
			'AwayTeam': ['TeamC', 'TeamD'],
			'FTR': ['H', 'A'],
			'B365H': [1.5, 2.0],
			'B365D': [3.5, 3.2],
			'B365A': [4.0, 3.8],
		}
		df = pd.DataFrame(data)
		expected_data = {
			'HomeTeam': ['TeamA', 'TeamB'],
			'AwayTeam': ['TeamC', 'TeamD'],
			'FTR': [1, 2],
			'B365H': [1.5, 2.0],
			'B365D': [3.5, 3.2],
			'B365A': [4.0, 3.8],
		}
		expected_df = pd.DataFrame(expected_data)

		result_df = preprocess_data(df)

		assert_frame_equal(result_df, expected_df)

	def test_define_features_and_target_success(self):
		data = {
			'Feature1': [1, 2, 3],
			'Feature2': [4, 5, 6],
			'Target': [0, 1, 0]
		}
		df = pd.DataFrame(data)
		features_columns = ['Feature1', 'Feature2']
		target_column = 'Target'

		expected_features = pd.DataFrame({
			'Feature1': [1, 2, 3],
			'Feature2': [4, 5, 6]
		})
		expected_target = pd.Series([0, 1, 0], name='Target')

		features, target = define_features_and_target(df, features_columns, target_column)

		pd.testing.assert_frame_equal(features, expected_features)
		pd.testing.assert_series_equal(target, expected_target)


if __name__ == '__main__':
	unittest.main()
