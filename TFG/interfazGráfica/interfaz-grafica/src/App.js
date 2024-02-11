import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ListaUsuarios from './listaUsuarios';
import PerfilUsuario from './PerfilUsuario';


function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 3000);
  }, []);

  if (loading) {
    return(
      <div>
      <img class="portada portada1" src="./logo512.png"/>
      <img class="portada portada2" src="./fontbolt.png"/>
      </div>
    );
  }

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
