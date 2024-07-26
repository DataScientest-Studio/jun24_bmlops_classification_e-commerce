# DAGs Directory

This directory contains Directed Acyclic Graphs (DAGs) and related scripts for orchestrating data processing and model training tasks. These DAGs are intended for use within the project and may be integrated with different workflow orchestration tools or frameworks.

## Directory Structure

dags/
│
├── features/ # Scripts related to feature engineering
│ ├── init.py # Initializes the features module
│ └── build_features.py # Contains classes for data importing and preprocessing
│
├── models/ # Scripts related to model training
│ ├── init.py # Initializes the models module
│ └── train_model.py # Contains classes for training machine learning models
│
├── my_dag.py # Example DAG definition for training and predictions
│
└── requirements.txt # Python dependencies for DAG scripts


## Key Files

- **`features/`**:
  - **`build_features.py`**:
    - **`DataImporter`**: Loads and splits data for training and validation.
    - **`TextPreprocessor`**: Handles text preprocessing tasks.
    - **`ImagePreprocessor`**: Manages image preprocessing tasks.

- **`models/`**:
  - **`train_model.py`**:
    - **`TextLSTMModel`**: Defines the LSTM model for text data.
    - **`ImageVGG16Model`**: Defines the VGG16 model for image data.
    - **`concatenate`**: Function for combining different feature representations.

- **`my_dag.py`**:
  - **Purpose**: Provides a sample DAG for training models and generating predictions. It demonstrates how to use the components in the `features` and `models` directories within a DAG framework.
  - **Key Functions**:
    - **`train_models()`**: Executes model training using the imported components.
    - **`make_predictions()`**: Runs predictions using the trained models.

- **`requirements.txt`**:
  - **Purpose**: Lists the Python dependencies required for running the DAG scripts. Ensure that all dependencies are installed to avoid runtime issues.
  - **Usage**: Install the dependencies by running `pip install -r requirements.txt`.

## Basic Usage

1. **Integration**: These DAGs can be integrated into various workflow systems or executed as standalone scripts, depending on your project setup.
2. **Customization**: Modify `my_dag.py` or other DAG files to fit specific project needs or to add additional functionality.
3. **Execution**: Run the DAG scripts according to your workflow requirements, either manually or through a workflow orchestration tool.

## Additional Information

- **Project Context**: This directory is part of the larger "movie_recommendation" project, which aims to build and deploy machine learning models for recommendation systems.
- **Dependencies**: Ensure that all necessary Python packages are installed as specified in `requirements.txt`.

For more detailed instructions on the overall project and its components, please refer to the main `README.md` file in the root of the project.

