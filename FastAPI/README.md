# FastAPI Component

This directory contains the FastAPI application for serving the machine learning model's predictions and managing related operations. It provides an API interface for interacting with the model and retrieving predictions.

## Directory Structure

fastapi/
│
├── models/
│ ├── best_weights.json # Serialized model weights
│ ├── best_weights.pkl # Serialized model weights
│ ├── mapper.json # Mapping file for target labels
│ ├── mapper.pkl # Mapping file for target labels
│ ├── tokenizer_config.json # Tokenizer configuration
│ └── tokenizer.pkl # Serialized tokenizer
│
├── Dockerfile # Dockerfile for FastAPI setup
├── init_db.sql # SQL script to initialize the database
├── main.py # Main FastAPI application script
└── requirements.txt # Python dependencies for the FastAPI app

## Key Files

- **`models/`**:

  - Contains serialized model files and configurations used for predictions.
  - **`best_weights.json`**, **`best_weights.pkl`**: Serialized weights of the trained model.
  - **`mapper.json`**, **`mapper.pkl`**: Mapping of labels for prediction results.
  - **`tokenizer_config.json`**, **`tokenizer.pkl`**: Configuration and serialized tokenizer for text preprocessing.

- **`Dockerfile`**:

  - Defines the Docker image for deploying the FastAPI application.

- **`init_db.sql`**:

  - SQL script for setting up the database schema required by the FastAPI application.

- **`main.py`**:

  - Main FastAPI application script.
  - Defines API endpoints for model prediction and other related functionalities.

- **`requirements.txt`**:
  - Lists Python dependencies needed to run the FastAPI application.

## Basic Usage

1. **Set Up the Environment**:

   - Install dependencies using `pip install -r requirements.txt`.

2. **Run the Application**:

   - Start the FastAPI server by executing:
     ```bash
     uvicorn main:app --reload
     ```
   - Access the API at `http://127.0.0.1:8000`.

3. **Database Initialization**:

   - Run the SQL script `init_db.sql` to set up the required database schema.

4. **Docker Setup**:
   - Build and run the Docker image using the provided `Dockerfile` if deploying in a containerized environment:
     ```bash
     docker build -t fastapi-app .
     docker run -p 8000:8000 fastapi-app
     ```

## Additional Information

The FastAPI component is designed to provide an API interface for the machine learning model. It allows for easy integration with other services and applications, facilitating model deployment and interaction.

For more detailed instructions and updates, please refer to the main `README.md` in the root of the project.
