# Machine Learning Project Workflow

This project outlines the workflow for a machine learning model training process, involving data retrieval, cross-validation experiments, and model training using optimal parameters.

## Project Steps

1. **Retrieve Data and Store in Google Cloud Storage**
    - The initial step involves collecting the necessary data from [football-data.co.uk](https://www.football-data.co.uk/) and securely storing it in Google Cloud Storage. This ensures that the data is easily accessible for subsequent processes.

2. **Cross-Validation Experiment**
    - Data is retrieved from Google Cloud Storage.
    - Cross-validation experiments are conducted to evaluate model performance across different configurations in Vertex AI.
    - The results of these experiments, including metrics and model parameters, are stored in [Neptune.ai](https://neptune.ai).

3. **Model Training with Best Parameters**
    - The best-performing parameters are retrieved from Neptune.ai.
    - Using these parameters, the final model is trained in Vertex AI.
    - The model is then stored back in Google Cloud Storage for further use.

4. **Inference**
    - The server Flask app is deployed.
    - It loads the model from the Google Cloud Storage.
    - Serves predictions.

## Flowchart

![Football match predictor Flowchart.png](Football%20match%20predictor%20Flowchart.png)

## Tools and Technologies

- **Google Cloud Storage**: Used for storing data and models.
- **Artifact Registry**: Used for storing custom Docker images.
- **Vertex AI**: Used for experiment running and model training.
- **Google Cloud Run**: Used for running the server Flask app.
- **Neptune.ai**: Used for tracking experiments and storing results.
- **Python/Scikit-learn**: Tools for custom model training and cross-validation.

## Usage

1. **Data Storage**: Upload your dataset to Google Cloud Storage.
2. **Experimentation**: Run cross-validation and log results to Neptune.ai.
3. **Model Training**: Train the model using the best parameters from Neptune.ai and store the model in Google Cloud Storage.
4. **Inference**: Serve predictions through Cloud Run.
