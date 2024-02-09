import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ListaUsuarios from './listaUsuarios';
import PerfilUsuario from './PerfilUsuario';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ListaUsuarios />} />
        <Route path="/perfil/:id" element={<PerfilUsuario />} />
      </Routes>
    </Router>
  );
}

export default App;
