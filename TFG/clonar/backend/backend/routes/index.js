const express = require("express");


const router = express.Router();

const userController = require('../controllers/Users');
const numeroController = require('../controllers/Users');

// Ruta para crear un usuario
router.post('/crear-usuario', userController.createUser);

// Ruta para crear un número
router.post('/crear-numero', numeroController.createNumero);

module.exports = router;








