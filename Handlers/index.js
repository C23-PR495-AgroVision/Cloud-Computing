const express = require('express');
const routes = require('./routes');
const bodyParser = require('body-parser');
const { initializeApp } = require('firebase/app');
const { getFirestore } = require('firebase/firestore');

const firebaseConfig = {
  // Firebase configuration
  apiKey: "AIzaSyBQv6Rg6Rx5uxbY3RpteS_JZ5LAedX195M",
  authDomain: "capstone-project-386912.firebaseapp.com",
  projectId: "capstone-project-386912",
  storageBucket: "capstone-project-386912.appspot.com",
  messagingSenderId: "529934951981",
  appId: "1:529934951981:web:b44fa616557068a17f3aa4",
  measurementId: "G-9H1H5R9LTY"
};

const app = express();
const port = 8080;

const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);

app.use(bodyParser.json());
app.use(express.json());
app.use('/', routes);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

module.exports = app;
