const express = require('express');
const firebaseAdmin = require('firebase-admin');

const router = express.Router();

// Inisialisasi Firebase menggunakan credential yang diberikan
const serviceAccount = require('./path/to/credential.json');
firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount),
  databaseURL: 'https://capstone-project-386912.firebaseio.com' // URL database Firebase Anda
});

// Route untuk menyimpan history prediksi
router.post('/', (req, res) => {
  // Dapatkan data pengguna dan history prediksi dari body request
  const { userId, history } = req.body;

  // Simpan history prediksi ke Firebase Realtime Database
  const db = firebaseAdmin.database();
  const userHistoryRef = db.ref('userHistory');
  userHistoryRef.child(userId).push().set(history);

  res.status(200).json({ message: 'User history saved successfully' });
});

module.exports = router;
