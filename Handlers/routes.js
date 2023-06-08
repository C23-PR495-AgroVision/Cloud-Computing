const express = require('express');
const router = express.Router();

const { signupRequest, signinRequest, signoutRequest, resetPasswordRequest, editNameRequest, addProfilePicture} = require('./userHandler');
const { userHistoryRequest } = require('../ModelsHandlers/userHistory');
// Import modul yang sesuai untuk signin dan signout

// Route untuk signup
router.post('/userHandler', signupRequest);

// Route untuk signin
router.post('/signin', signinRequest);

// Route untuk reset password
router.post('/reset-password', resetPasswordRequest);

// Route untuk edit nama
router.post('/edit-name', editNameRequest);

// Route untuk menambahkan foto profil
router.put('/profile/picture', addProfilePicture);

// Route untuk signout
router.post('/signout', signoutRequest);
// Route untuk getUserData

router.get('/user/:uid', async (req, res) => {
    const uid = req.params.uid;
    const result = await getUserData(uid);
    
    res.status(200).json(result);
  });

// route untuk user history
router.post('/userHistory', userHistoryRequest);
// Tambahkan rute lainnya sesuai kebutuhan

module.exports = router;
