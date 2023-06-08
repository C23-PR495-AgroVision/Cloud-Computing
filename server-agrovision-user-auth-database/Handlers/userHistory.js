const express = require('express');
const app = express();
const admin = require('firebase-admin');
const { Storage } = require('@google-cloud/storage');
const sharp = require('sharp');
const { v4: uuidv4 } = require('uuid');

const serviceAccount = require('./service-account-key.json');
const storage = new Storage({
  projectId: 'your-project-id',
  keyFilename: 'service-account-key.json',
});
const bucket = storage.bucket('your-bucket-name');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://your-project-id.firebaseio.com',
});
const db = admin.firestore();

const models = {
  apple: {
    path: 'saved-models/Apple_MobileNetV2_model2_Based_Non_Augmented',
    classNames: ['Apple Black rot', 'Apple Scab Leaf', 'Apple leaf Healthy', 'Apple rust leaf'],
  },
  bellpepper: {
    path: 'saved-models/BellPaper_MobileNetV2_model2_Based_Non_Augmented',
    classNames: ['Pepper bell Bacterial spot', 'Pepper bell healthy'],
  },
  cherry: {
    path: 'saved-models/Cherry_MobileNetV2_model2_Based_Non_Augmented',
    class_names: ['healthy', 'powdery_mildew']
  },
    corn: {
    path: 'saved-models/Corn_MobileNetV2_model2_Based_Non_Augmented',
    class_names: ['Corn Gray leaf spot', 'Corn healthy', 'Corn leaf blight', 'Corn rust leaf']
  },
   grape: {
    path: 'saved-models/Grape_MobileNetV2_model2_Based_Non_Augmented',
    class_names: ['Grape Esca (Black_Measles)', 'Grape Leaf blight (Isariopsis_Leaf_Spot)', 'grape leaf Healthy', 'grape leaf black rot']
  },
   peach: {
    path: 'saved-models/Peach_MobileNetV2_model2_Based_Non_Augmented',
    class_names: ['Peach___Bacterial_spot', 'Peach___healthy']
}  // Tambahkan model lainnya di sini
};


app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.post('/predict/:modelName', async (req, res) => {
  const { modelName } = req.params;
  const { image, userId } = req.body;

  if (!models[modelName]) {
    return res.status(400).json({ error: 'Invalid model name' });
  }

  const modelPath = models[modelName].path;
  const classNames = models[modelName].classNames;

  // Simpan gambar ke Google Cloud Storage
  const imageBuffer = Buffer.from(image, 'base64');
  const filename = `${uuidv4()}.jpg`;
  const file = bucket.file(filename);

  await sharp(imageBuffer)
    .resize(224, 224)
    .toFile(file.createWriteStream());

  // Prediksi menggunakan model TensorFlow
  const model = await tf.loadLayersModel(`file://${modelPath}`);
  const img = await tf.keras.preprocessing.image.loadImg(`gs://${bucket.name}/${filename}`);
  const processedImg = await tf.image.resizeBilinear(tf.expandDims(img), [224, 224]);
  const predictions = await model.predict(processedImg);
  const predictedClass = classNames[predictions.argMax().dataSync()[0]];

  // Simpan riwayat prediksi ke Firestore
  const predictionRef = db.collection('predictions').doc();
  await predictionRef.set({
    userId,
    modelName,
    predictedClass,
    confidence: predictions.max().dataSync()[0],
  });

  res.json({
    class: predictedClass,
    confidence: predictions.max().dataSync()[0],
  });
});

app.get('/ping', (req, res) => {
  res.send('Hello, I am alive');
});

app.listen(8000, () => {
  console.log('Server started on port 8000');
});
