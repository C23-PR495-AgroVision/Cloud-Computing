from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from skimage import transform
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "capstone-project-386912",
  "private_key_id": "afcc808b26f14e8726df30220e4f0ddabcef5cd6",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQC1qnYUhg27Ffkw\nWf3ZIqkqTiqZActDU1FCpHzu880aXFrC0xve7rGHcGRxtnBhwZGCaRhLEpZbzV97\nMoiCHBfxSimAMr8814dhaLkbSS0Z6StRrPqUOMwq2i8ynhLakzLJMlHOFQ21qIqc\nVyYWH15qpVkwjer50ZNHMIAbsc3WGibJov4NLtEFJ1tvN7TOvxyfzFrWKkeYG4q8\nH4ynyc2+N/znN1focaEaXvLmmIdKhPSNdlIBUeKGywQD9Gm8n/5HqQ7b19oSCG4z\nHD75c6VnxtLhBJMNY3DLbYU/pOkus8hVSu2kuMaemV2unpY0XibMr0XtoaJS2PH6\n6yY1IGjXAgMBAAECgf9iSFaZw+ypyrmF7ynmz1m2CZQCM3ZEdk8APv1YSY4tNMnl\nnVD2yyxAmg29d3ZVbOPMKg96jhPKltGRVUWFHq3VXMoXEV1lDTWw/Xcny+8alYta\nJLtsdU3/4Qqn191bY0eWkiKv27QPE5/p9Twlu9LY35vhKOZ3QWrsmNC2KvuxWItD\nJrtElGqyBbGM2x96MF6qpjnV/tWLpreZ9/LPWB0TkZ7KPXde8fJxdbI+twTunSTZ\ncFTsXVD5B4icpalnEn4esKsi0UAU6U0hAb99QNZWuHay7ZX731mILgvj18+jmn+b\nG+stWElEBrWveKTHwwln03Hqm8s71o3vT/zPNZkCgYEA20pr4+zCA2LmAyjweo2i\nE9ovE240K5TWodaUpui8vTd1VSNeuytWaZ4PcBytiYezm53YL7rzHN8dpFp3zhf6\n8wFxO4qGXF6U/bQGI36gGV0UfjQqnFxHCqLKecYKi1ryDr7Oy/3JwQlvbbl6RC6l\nUkhX9c81JpiV7icOD1pKC0kCgYEA1BOmBBh0x5SBUavY7drgUgy90vxYruIGgOur\nJtlPv1g2vUhDWCTHc8OlM9q3rCkoFJ02SkUVUYISGSmdX3qfsUXhV8xC6gR7DJwX\nQk2J7sKAyjIicrIctOQxOY4jsuKzm6BzxLRPNIMG3RUnaKl6UtI6A+MtP/JkrV+p\nenEdsx8CgYAcRjI3BxXU3fGOQr8O7igRqzYaqUDsxZoO793mz2dWdkoYmiDivSm9\nIHYZHHl7nBWaYPW44b/q3xGxWUDNP+ZJYsw4wxmj20YWmBmahf8ahhfYVd2Qn41B\nX8//d3twkF9Za1y6jJRw4UiOuzV6iREj1NQSi47s1Quv0zVK4XdekQKBgCcqRcOF\n3LMq6sLxcItkm36rmbbIIXySg071ttLi2QZmPR2xpbY2fJsVa4HrB3aE10EPU4Jd\nxbUax0rcU5LZa3pqhFYZg9YB49ONVAJLnYh5ZR1yKshxujlx1uFhLZiQo0i/VgHi\npqn09KSJjpCWk9+NsWccYjPoCM231+2jzC9TAoGAZ53qpqQNw1zl9K36gUFRwySO\nzXAtxty93MgG7xtDBoJ4xCT0DEuxgN6Bx8STlCy8UQ7gjg9Pm0V5IFcf0Nr4QYCH\nld5ZqOzegJi6V0HXJ/2fHAb34ZQ79rIRbq0qDRqe/VrpOClHWRrmlRJYjThWBxGs\nXg7NW25B8Lp5YiVP/q0=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-6klxu@capstone-project-386912.iam.gserviceaccount.com",
  "client_id": "116250413624762425131",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-6klxu%40capstone-project-386912.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred)
db = firestore.client()

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

def save_prediction_to_firestore(model_name, predicted_class, confidence):
    doc_ref = db.collection('predictions').document()
    doc_ref.set({
        'model_name': model_name,
        'predicted_class': predicted_class,
        'confidence': confidence
    })
    print('Hasil prediksi berhasil disimpan di Firestore.')

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
    confidence = float(np.max(predictions[0]))

    save_prediction_to_firestore(model_name, predicted_class, confidence)

    return {
        'class': predicted_class,
        'confidence': confidence
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
