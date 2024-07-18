from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import json
from tensorflow import keras

app = FastAPI()

class ProductData(BaseModel):
    description: str
    image: str  # base64 encoded image string

# Load tokenizer configuration
with open("models/tokenizer_config.json", "r", encoding="utf-8") as json_file:
    tokenizer_config = json_file.read()
tokenizer = keras.preprocessing.text.tokenizer_from_json(tokenizer_config)

# Load models
text_model = tf.keras.models.load_model('models/best_lstm_model.keras')
image_model = tf.keras.models.load_model('models/best_vgg16_model.keras')

# Load best weights
with open("models/best_weights.json", "r", encoding="utf-8") as json_file:
    best_weights = json.load(json_file)

# Load mapper
with open("models/mapper.json", "r", encoding="utf-8") as json_file:
    mapper = json.load(json_file)

def preprocess_text(text):
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = keras.preprocessing.sequence.pad_sequences(
        sequences, maxlen=10, padding="post", truncating="post"
    )
    return padded_sequences

def preprocess_image(image_base64):
    import base64
    from io import BytesIO
    from PIL import Image

    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data)).resize((224, 224))
    img_array = keras.preprocessing.image.img_to_array(image)
    img_array = keras.applications.vgg16.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

@app.post("/api/predict")
def predict(data: ProductData):
    try:
        text_input = preprocess_text(data.description)
        image_input = preprocess_image(data.image)

        lstm_proba = text_model.predict(text_input)
        vgg16_proba = image_model.predict(image_input)

        concatenate_proba = (
            best_weights[0] * lstm_proba + best_weights[1] * vgg16_proba
        )
        final_predictions = np.argmax(concatenate_proba, axis=1)

        return {"prediction": mapper[str(final_predictions[0])]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
