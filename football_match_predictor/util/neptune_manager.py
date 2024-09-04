import neptune

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('NEPTUNE_API_KEY')
project_name = "majkellvz/football-match-predictor"


def init_neptune():
	run = neptune.init_run(
		project=project_name,
		api_token=api_key)
	return run


def init_project():
	run = neptune.init_project(
		project=project_name,
		mode="read-only",
		api_token=api_key
	)
	return run
