from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from skimage import transform
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS = {
    "apple": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/apple_xception",
        "class_names": ["good", "bad"],
    },
    "banana": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/banana_xception",
        "class_names": ["overripe", "ripe", "rotten", "unripe"],
    },
    "guava": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/guava_xception",
        "class_names": ["bad", "good"],
    },
    "lime": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/lime_xception",
        "class_names": ["bad", "good"],
    },
    "orange": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/orange_xception",
        "class_names": ["bad", "good"],
    },
    "pomegranate": {
        "path": "fastapi-image-recognition-fruit-ripness/saved-models/pomegranate_xception",
        "class_names": ["bad", "good"]
    }
}

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.on_event("startup")
async def startup_event():
    app.models = {}
    for model_name, model_config in MODELS.items():
        model = load_model(model_config["path"])
        app.models[model_name] = model

@app.post("/predict/{model_name}")
async def predict(
    model_name: str,
    file: UploadFile = File(...)
):
    if model_name not in app.models:
        return {"error": "Invalid model name"}

    model = app.models[model_name]

    image = read_file_as_image(await file.read())
    image = transform.resize(image, (224, 224, 3))
    img_batch = np.expand_dims(image, 0)
    
    predictions = model.predict(img_batch)

    class_names = MODELS[model_name]["class_names"]
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
