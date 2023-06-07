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
        "path": "fastapi-image-recognition-plant-diseases/saved-models/Apple_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["Apple Black rot", "Apple Scab Leaf", "Apple leaf Healthy", "Apple rust leaf"],
    },
    "bellpepper": {
        "path": "fastapi-image-recognition-plant-diseases/saved-models/BellPaper_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["Pepper bell Bacterial spot", "Pepper bell healthy"]
    },
    "cherry": {
        "path": "fastapi-image-recognition-plant-diseases/saved-models/Cherry_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["healthy", "powdery_mildew"]
    },
    "corn": {
        "path": "fastapi-image-recognition-plant-diseases/saved-models/Corn_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["Corn Gray leaf spot", "Corn healthy", "Corn leaf blight", "Corn rust leaf"]
    },
    "grape": {
        "path": "fastapi-image-recognition-plant-diseases/saved-models/Grape_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["Grape Esca (Black_Measles)", "Grape Leaf blight (Isariopsis_Leaf_Spot)", "grape leaf Healthy", "grape leaf black rot"]
    },
    "peach": {
        "path": "fastapi-image-recognition-plant-diseases/saved-models/Peach_MobileNetV2_model2_Based_Non_Augmented",
        "class_names": ["Peach___Bacterial_spot", "Peach___healthy"]
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
