import hashlib


def generate_hash(start_year: int, end_year: int) -> str:
	data_string = f"{start_year}_{end_year}"
	return hashlib.md5(data_string.encode()).hexdigest()


def generate_model_hash(params: dict, start_year: int, end_year: int) -> str:
	params_string = str(params)
	data_string = f"{params_string}_{start_year}_{end_year}"
	return hashlib.md5(data_string.encode()).hexdigest()
