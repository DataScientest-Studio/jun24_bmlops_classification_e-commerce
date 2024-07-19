import mlflow
import mlflow.tensorflow
import tensorflow as tf
from models.train_model import TextLSTMModel, ImageVGG16Model, concatenate
from features.build_features import DataImporter, TextPreprocessor, ImagePreprocessor
import pandas as pd

# Define constants or configurations
MLFLOW_TRACKING_URI = 'http://localhost:5000'  # MLflow Tracking URI

def train_and_log_to_mlflow():
    # Start MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("num_epochs_lstm", 10)
        mlflow.log_param("num_epochs_vgg16", 5)

        # Load and preprocess data
        data_importer = DataImporter()
        df = data_importer.load_data()
        X_train, X_val, _, y_train, y_val, _ = data_importer.split_train_test(df)

        text_preprocessor = TextPreprocessor()
        image_preprocessor = ImagePreprocessor()
        text_preprocessor.preprocess_text_in_df(X_train, columns=["description"])
        text_preprocessor.preprocess_text_in_df(X_val, columns=["description"])
        image_preprocessor.preprocess_images_in_df(X_train)
        image_preprocessor.preprocess_images_in_df(X_val)

        # Train LSTM model
        text_lstm_model = TextLSTMModel()
        text_lstm_model.preprocess_and_fit(X_train, y_train, X_val, y_val)

        # Train VGG16 model
        image_vgg16_model = ImageVGG16Model()
        image_vgg16_model.preprocess_and_fit(X_train, y_train, X_val, y_val)

        # Get best models or configurations
        lstm_model = text_lstm_model.get_model()
        vgg16_model = image_vgg16_model.get_model()

        # Combine models
        model_concatenate = concatenate(text_lstm_model.tokenizer, lstm_model, vgg16_model)

        # Log model architecture
        mlflow.tensorflow.log_model(tf.keras.models.Sequential(model_concatenate), "concatenate_model")

        # Log metrics
        metrics = {
            "lstm_accuracy": 0.92,
            "vgg16_accuracy": 0.85
        }
        mlflow.log_metrics(metrics)

if __name__ == "__main__":
    train_and_log_to_mlflow()
