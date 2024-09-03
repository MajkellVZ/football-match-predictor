import json
import os


def get_parameters():
	config_path = os.path.join(os.path.dirname(__file__), "../config/input.json")

	with open(config_path, "r") as config_file:
		config = json.load(config_file)

	start_year = config.get("start_year")
	end_year = config.get("end_year")

	return start_year, end_year
