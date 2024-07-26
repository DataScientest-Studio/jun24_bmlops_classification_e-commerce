# Airflow Component

This directory contains the Apache Airflow setup for orchestrating data processing pipelines in the project. It automates the workflow of model training and prediction.

## Directory Structure

airflow/
│
├── dags/
│ └── my_dag.py # Defines the Airflow DAG and tasks
│
├── features/
│ ├── **init**.py # Initializes the features module
│ └── build_features.py # Scripts for data importing and preprocessing
│
├── Dockerfile # Dockerfile for Airflow setup
└── requirements.txt # Python dependencies for Airflow tasks

## Key Files

- **`my_dag.py`**:
  - Schedules two main tasks:
    - `train_models_task`: Trains machine learning models using the prepared dataset.
    - `make_predictions_task`: Generates predictions based on the trained models.
- **`build_features.py`**:
  - `DataImporter`: Loads and splits data for training and validation.
  - `TextPreprocessor` and `ImagePreprocessor`: Preprocess text and image data respectively.

## Basic Usage

- This Airflow component is part of a larger MLOps pipeline. The DAG `ml_training_and_prediction` is designed to automate model training and prediction processes.

- **Docker Setup**:
  - Use the provided `Dockerfile` to build and deploy the Airflow environment if needed.

## Additional Information

This component is part of a project template based on MLOps practices, focusing on the subject "movie_recommendation." Adjustments may be needed to fit specific project requirements.

For more detailed instructions and updates, please refer to the main `README.md` in the root of the project.
