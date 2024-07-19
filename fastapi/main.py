from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
import logging
import sqlite3
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uvicorn
from typing import Optional


# Initialize FastAPI app
app = FastAPI()

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Load models and configurations
with open("models/tokenizer_config.json", "r", encoding="utf-8") as json_file:
    tokenizer_config = json_file.read()
tokenizer = keras.preprocessing.text.tokenizer_from_json(tokenizer_config)

text_model = tf.keras.models.load_model('models/best_lstm_model.keras')
image_model = tf.keras.models.load_model('models/best_vgg16_model.keras')

with open("models/best_weights.json", "r", encoding="utf-8") as json_file:
    best_weights = json.load(json_file)

with open("models/mapper.json", "r", encoding="utf-8") as json_file:
    mapper = json.load(json_file)

# Setup logging
logging.basicConfig(level=logging.INFO)

class ProductData(BaseModel):
    description: str
    image: str  # base64 encoded image string

class NewProductData(BaseModel):
    description: str
    image: str  # base64 encoded image string
    category: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # This example uses hardcoded credentials for simplicity
    # In production, use a proper database and hashed passwords
    if form_data.username == "user" and form_data.password == "password":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=400, detail="Incorrect username or password"
    )

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

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/api/predict")
def predict(data: ProductData, token: str = Depends(oauth2_scheme)):
    try:
        text_input = preprocess_text(data.description)
        image_input = preprocess_image(data.image)

        lstm_proba = text_model.predict(text_input)
        vgg16_proba = image_model.predict(image_input)

        concatenate_proba = (
            best_weights[0] * lstm_proba + best_weights[1] * vgg16_proba
        )
        final_predictions = np.argmax(concatenate_proba, axis=1)

        prediction = mapper[str(final_predictions[0])]
        
        # Save prediction to the database
        conn = get_db_connection()
        conn.execute("INSERT INTO predictions (description, image, prediction) VALUES (?, ?, ?)",
                     (data.description, data.image, prediction))
        conn.commit()
        conn.close()

        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/data-ingest")
def data_ingest(new_data: NewProductData, token: str = Depends(oauth2_scheme)):
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO products (description, image, category) VALUES (?, ?, ?)",
                     (new_data.description, new_data.image, new_data.category))
        conn.commit()
        conn.close()
        return {"message": "Data ingested successfully"}
    except Exception as e:
        logging.error(f"Data ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/monitor")
def monitor(token: str = Depends(oauth2_scheme)):
    try:
        # Example: return model metrics and health status
        metrics = {
            "model_name": "best_lstm_model.keras",
            "accuracy": 0.95,  # Example metric
            "status": "healthy"
        }
        return metrics
    except Exception as e:
        logging.error(f"Monitoring error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
