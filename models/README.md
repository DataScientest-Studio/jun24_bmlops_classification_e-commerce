# Models Directory

This directory contains the machine learning models used in the project. It includes trained models and associated files for model management.

## Directory Structure

models/
│
├── best_weights.json # JSON file with the best model weights (if applicable)
├── best_weights.pkl # Pickle file with the best model weights (if applicable)
├── mapper.json # JSON file with mappings used in the model (e.g., labels to indices)
├── mapper.pkl # Pickle file with mappings used in the model
├── tokenizer_config.json # JSON file with tokenizer configuration
└── tokenizer.pkl # Pickle file with the tokenizer object

## Key Files

- **`best_weights.json`** and **`best_weights.pkl`**:

  - These files store the best weights for the trained models. They are used to load the model with the highest performance metrics.

- **`mapper.json`** and **`mapper.pkl`**:

  - Contain mappings used by the model, such as label encodings or other necessary mappings for model predictions.

- **`tokenizer_config.json`** and **`tokenizer.pkl`**:
  - **`tokenizer_config.json`**: Contains configuration details for the tokenizer used in text processing.
  - **`tokenizer.pkl`**: Stores the actual tokenizer object used to preprocess text data.

## Managing Models

1. **Loading Models**:

   - Ensure that you load the appropriate model weights and configurations for your tasks. Use the files in this directory to restore the model to its trained state.

2. **Updating Models**:

   - When retraining models, save the new weights and configurations in this directory, replacing the existing files as needed.

3. **Tokenizers**:

   - Use the tokenizer files for text preprocessing. Ensure that the configuration matches the one used during training.

4. **Mapper Files**:
   - Use the mapper files to handle label encodings or other mappings necessary for model predictions.

## Additional Information

The `models` directory is a crucial part of the machine learning pipeline. It stores models and related files needed for predictions and evaluations. Make sure to keep the directory organized and up-to-date with the latest model artifacts.

For more detailed instructions and updates, please refer to the main `README.md` in the root of the project.
