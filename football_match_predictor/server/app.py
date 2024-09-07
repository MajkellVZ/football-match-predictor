import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from football_match_predictor.model.predict import Predictor
from football_match_predictor.util.logger import Logger

app = Flask(__name__)
CORS(app)
logger = Logger(name="predictor", level=logging.DEBUG)

predictor = Predictor('models/model.pickle')


@app.route('/predict', methods=['POST'])
def predict():
	try:
		data = request.get_json()
		home_team = data['home_team']
		away_team = data['away_team']
		features = pd.DataFrame(data['features'])

		result = predictor.predict(home_team, away_team, features)
		return jsonify(result)

	except Exception as e:
		logger.error(f"Prediction failed: {str(e)}")
		return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
	app.run(debug=True)
