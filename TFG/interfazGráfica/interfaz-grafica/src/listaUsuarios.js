// ListaUsuarios.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


function ListaUsuarios({ onSelectUser }) {
  const [usuarios, setUsuarios] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const navigate = useNavigate();
  


  useEffect(() => {
    fetch('http://localhost:3001/getUsers')
      .then(response => response.json())
      .then(data => setUsuarios(data))
      .catch(error => console.error('Error fetching users:', error));
  }, []);

  const procesarBiografia = (texto) => {
    let biografiaProcesada = texto.replace(/\\n/g, '<br>');
    biografiaProcesada = biografiaProcesada.replace(/\\x(\w\w)/g, (match, p1) => String.fromCharCode(parseInt(p1, 16)));
    return biografiaProcesada;
  };

  const handleBusquedaChange = (event) => {
    setBusqueda(event.target.value);
  };

  const abrirPerfil = (usuario) => {
    navigate(`/perfil/${usuario.id}`);
  };

  const usuariosFiltrados = usuarios.filter(usuario =>
    usuario.nickname.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div>
      <div className="bar">
        <img class="logoImg" src="./fontbolt.png"/>
        <div className="wrap">
          <div className="search">
            <input type="text" className="searchTerm" placeholder="Busca por nombre de usuario" value={busqueda} onChange={handleBusquedaChange} />
            <button type="submit" className="searchButton">
              <i className="fa fa-search"></i>
            </button>
          </div>
        </div>
      </div>
      <br></br>
      <br></br>
      <br></br>
      <ul>
        {usuariosFiltrados.map(usuario => (
          <li key={usuario.id} >
            <div className="tarjeta">
              <div className="container">
                <div className="profile">
                  <div className="profile-image">
                    <img src={`http://localhost:3001/${usuario.fotoPerfil}`} alt="" />
                  </div>
                  <div className="profile-user-settings">
                    <h1 className="profile-user-name">{usuario.nickname}</h1>
                    <button className="btn profile-edit-btn" onClick={() => abrirPerfil(usuario)}>Acceder al perfil</button>
                  </div>
                  <div className="profile-stats">
                    <ul>
                      <li><span className="profile-stat-count">{usuario.postNum} </span> posts</li>
                      <li><span className="profile-stat-count">{usuario.followersNum}</span> followers</li>
                      <li><span className="profile-stat-count">{usuario.followingNum}</span> following</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ListaUsuarios;
