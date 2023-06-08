const express = require('express');
const router = express.Router();

const { signupRequest, signinRequest, signoutRequest} = require('./userHandler');
const { userHistoryRequest } = require('ModelsHandlers/userHistory.js');
// Import modul yang sesuai untuk signin dan signout

// Route untuk signup
router.post('/userHandler', signupRequest);

// Route untuk signin
router.post('/signin', signinRequest);

// Route untuk signout
router.post('/signout', signoutRequest);

// route untuk user history
router.post('/userHistory', userHistoryRequest);
// Tambahkan rute lainnya sesuai kebutuhan

module.exports = router;
