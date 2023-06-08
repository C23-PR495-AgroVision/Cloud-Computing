const { initializeApp } = require('firebase/app');
const { getFirestore, collection, setDoc, addDoc } = require('firebase/firestore');
const { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } = require('firebase/auth');
const { doc } = require('firebase/firestore'); // Tambahkan baris ini

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

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

const signupRequest = (request, response) => {
  const { emailField, fullnameField, passwordField } = request.body;

  if (!emailField || !fullnameField || !passwordField) {
    return response.status(400).json({
      status: 'fail',
      message: 'All fields need to be filled. (Email, Full name, and Password)',
    });
  }

  createUserWithEmailAndPassword(auth, emailField, passwordField)
    .then((userCred) => {
      console.log(userCred.user);
      const email = emailField;
      const name = fullnameField;
      const password = passwordField;
      const userFirebaseID = doc(db, "accounts", userCred.user.uid); // Perbarui baris ini
      
      const accountsCollection = collection(db, 'accounts');
      addDoc(accountsCollection, { email, name, password })
        .then((docRef) => {
            console.log('Document written with ID: ', docRef.id);
          return response.status(201).json({
            status: 'success',
            message: 'Sign-up has been successful',
          });
        })
        .catch((error) => {
          console.error('Error writing document:', error);
          return response.status(500).json({
            status: 'fail',
            message: 'An error occurred during sign-up',
          });
        });
    })
    .catch((error) => {
      console.error('Error creating user:', error);
      return response.status(500).json({
        status: 'fail',
        message: 'An error occurred during sign-up',
      });
    });
};

const signinRequest = (request, response) => {
  const { email, password } = request.body;

  if (!email || !password) {
    return response.status(400).json({
      status: 'fail',
      message: 'Email and password are required.',
    });
  }

  signInWithEmailAndPassword(auth, email, password)
    .then((userCred) => {
      console.log(userCred.user);
      return response.status(200).json({
        status: 'success',
        message: 'Sign-in successful',
        user: {
          email: userCred.user.email,
          name: userCred.user.name,
          // Include any other user data you want to return
        },
      });
    })
    .catch((error) => {
      console.error('Error signing in:', error);
      return response.status(500).json({
        status: 'fail',
        message: 'An error occurred during sign-in',
      });
    });
};

const signoutRequest = (request, response) => {
  auth.signOut()
    .then(() => {
      return response.status(200).json({
        status: 'success',
        message: 'Sign-out successful',
      });
    })
    .catch((error) => {
      console.error('Error signing out:', error);
      return response.status(500).json({
        status: 'fail',
        message: 'An error occurred during sign-out',
      });
    });
};

module.exports = {
  signupRequest,
  signinRequest,
  signoutRequest,
};