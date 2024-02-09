const express = require("express");


const router = express.Router();

const userController = require('../controllers/Users');
const numeroController = require('../controllers/Users');

// Ruta para crear un usuario
router.post('/crear-usuario', userController.createUser);

// Ruta para crear un número
router.post('/crear-numero', numeroController.createNumero);

//Get de datos generales del usuario
router.get('/getUsers',numeroController.getUsersSummary);

//get datos específicos de un ususario
router.get('/getEspecifiedUsers/:id',numeroController.getUserDetails);


router.post('/abrirSesion',numeroController.abrirSesion)


module.exports = router;








