from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from features.build_features import DataImporter, TextPreprocessor, ImagePreprocessor
from models.train_model import TextLSTMModel, ImageVGG16Model, concatenate
import tensorflow as tf
import pandas as pd
import json


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Initialize the DAG
dag = DAG(
    'ml_training_and_prediction',
    default_args=default_args,
    description='A DAG to train models and make predictions',
    schedule_interval='@daily',  # Run daily
    catchup=False  # Don't run backfilling
)


def train_models():
    data_importer = DataImporter()
    df = data_importer.load_data()
    X_train, X_val, _, y_train, y_val, _ = data_importer.split_train_test(df)

    # Preprocess text and images
    text_preprocessor = TextPreprocessor()
    image_preprocessor = ImagePreprocessor()
    text_preprocessor.preprocess_text_in_df(X_train, columns=["description"])
    text_preprocessor.preprocess_text_in_df(X_val, columns=["description"])
    image_preprocessor.preprocess_images_in_df(X_train)
    image_preprocessor.preprocess_images_in_df(X_val)

    # Train LSTM model
    print("Training LSTM Model")
    text_lstm_model = TextLSTMModel()
    text_lstm_model.preprocess_and_fit(X_train, y_train, X_val, y_val)
    print("Finished training LSTM")

    # Train VGG16 model
    print("Training VGG16 Model")
    image_vgg16_model = ImageVGG16Model()
    image_vgg16_model.preprocess_and_fit(X_train, y_train, X_val, y_val)
    print("Finished training VGG16")

train_models_task = PythonOperator(
    task_id='train_models_task',
    python_callable=train_models,
    dag=dag
)

def make_predictions():
    from predict import main as predict_main  # Import the predict script main function
    
    # Run the prediction script
    os.system("python predict.py --dataset_path data/preprocessed/X_train_update.csv --images_path data/raw/image_train")

make_predictions_task = PythonOperator(
    task_id='make_predictions_task',
    python_callable=make_predictions,
    dag=dag
)



train_models_task >> make_predictions_task

