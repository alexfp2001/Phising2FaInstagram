const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Establece la carpeta de archivos estáticos (donde se encuentra tu HTML, CSS, imágenes, etc.)
app.use(express.static(path.join(__dirname, 'instagram')));



// Maneja todas las rutas y sirve tu archivo HTML
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'instagram', 'index.html'));
});

// Inicia el servidor
app.listen(PORT, () => {
    console.log(`Servidor web escuchando en el puerto ${PORT}`);
});
