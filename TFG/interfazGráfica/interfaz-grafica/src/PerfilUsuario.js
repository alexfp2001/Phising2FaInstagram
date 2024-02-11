import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './PerfilUsuario.css';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap';

function PerfilUsuario() {
    const [usuario, setUsuario] = useState(null);
    const [loading, setLoading] = useState(true);
    const [modalOpen, setModalOpen] = useState(false);
    const [currentMediaIndex, setCurrentMediaIndex] = useState(null);
    const { id } = useParams();

    const [modalFollowers, setModalFollowers] = useState(false);
    const [modalFollowing, setModalFollowing] = useState(false);
    const [modalContacts, setModalContacts] = useState(false);
    const [modalPosts, setModalPosts] = useState(false);
    const [showSensitiveData, setShowSensitiveData] = useState(false);
    

    const toggleFollowers = () => setModalFollowers(!modalFollowers);
    const toggleFollowing = () => setModalFollowing(!modalFollowing);
    const toggleContacts = () => setModalContacts(!modalContacts);
    const toggleSensitiveData = () => {setShowSensitiveData(!showSensitiveData);};

    useEffect(() => {
        fetch(`http://localhost:3001/getEspecifiedUsers/${id}`)
            .then(response => response.json())
            .then(data => {
                if (data.rutaPublicaciones) {
                    data.rutaPublicaciones = JSON.parse(data.rutaPublicaciones);
                }
                setUsuario(data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching user:', error);
                setLoading(false);
            });
    }, [id]);



    const procesarBiografia = (texto) => {
        let biografiaProcesada = texto.replace(/\\n/g, '<br>');
        biografiaProcesada = biografiaProcesada.replace(/\\x(\w\w)/g, (match, p1) => String.fromCharCode(parseInt(p1, 16)));
        return biografiaProcesada;
    };

    const openModal = (index) => {
        setCurrentMediaIndex(index);
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
        setCurrentMediaIndex(null);
    };

    const nextMedia = () => {
        if (usuario && usuario.rutaPublicaciones && currentMediaIndex !== null) {
            setCurrentMediaIndex((currentMediaIndex + 1) % (usuario.rutaPublicaciones.length - 1));
        }
    };

    const previousMedia = () => {
        if (usuario && usuario.rutaPublicaciones && currentMediaIndex !== null) {
            setCurrentMediaIndex((currentMediaIndex - 1 + usuario.rutaPublicaciones.length - 1) % (usuario.rutaPublicaciones.length - 1));
        }
    };
    

    const renderMedia = (ruta, index) => {
        // Ignore first image (profile image) for modal gallery
        if (index === 0) return null;

        return (
            <div onClick={() => openModal(index - 1)} className="custom-gallery-item" key={index} tabIndex="0">
                {ruta.endsWith('.mp4') ? (
                    <video className="custom-gallery-video">
                        <source src={`http://localhost:3001/${ruta}`} type="video/mp4" />
                        Tu navegador no soporta videos HTML5.
                    </video>
                ) : (
                    <img src={`http://localhost:3001/${ruta}`} className="custom-gallery-image" alt="" />
                )}
            </div>
        );
    };
    

    const renderProfileImage = (ruta) => {
        return ruta.endsWith('.mp4') ? (
            <video className="custom-profile-video" controls>
                <source src={`http://localhost:3001/${ruta}`} type="video/mp4" />
                Tu navegador no soporta videos HTML5.
            </video>
        ) : (
            <img src={`http://localhost:3001/${ruta}`} className="custom-profile-image" alt="Perfil" />
        );
    };

    const renderModalContent = () => {
        if (!usuario || currentMediaIndex === null) return null;
        const ruta = usuario.rutaPublicaciones[currentMediaIndex + 1]; // Offset by 1 due to profile image
        if (ruta.endsWith('.mp4')) {
            return (
                <video className="custom-modal-video" controls autoPlay>
                    <source src={`http://localhost:3001/${ruta}`} type="video/mp4" />
                    Tu navegador no soporta videos HTML5.
                </video>
            );
        } else {
            return <img src={`http://localhost:3001/${ruta}`} className="custom-modal-image" alt="" />;
        }
    };

    const handleOpenSession = async () => {
        const url = 'http://localhost:3001/abrirSesion'; // Reemplaza con la URL de tu backend
        const session = { clave: usuario.sessionid }; // Reemplaza con los datos que deseas enviar
      
        try {
          const response = await fetch(url, {
            method: 'POST', // Método POST
            headers: {
              'Content-Type': 'application/json', // Especifica el tipo de contenido
            },
            body: JSON.stringify(session), // Convierte tus datos a un string JSON
          });
      
          if (!response.ok) {
            throw new Error('La respuesta de la red no fue ok');
          }
      
          const responseData = await response.json(); // O .text() si esperas una respuesta en texto plano
          console.log('Respuesta del servidor:', responseData);
        } catch (error) {
          console.error('Hubo un error al enviar la solicitud:', error);
        }
      };;

    if (loading) {
        return <div>Cargando...</div>;
    }
    if (!usuario) {
        return <div>No se encontró el usuario.</div>;
    }
    const followersList = usuario.followersList ? JSON.parse(usuario.followersList) : [];
    const followingList = usuario.followingList ? JSON.parse(usuario.followingList) : [];
    const listaContactosPr = usuario.lista_contactos ? JSON.parse(usuario.lista_contactos) : [];
    const listaContactos = listaContactosPr.map(contacto => procesarBiografia(contacto));
    

    return (
        <div className="custom-body">
            <header>
                <div className="custom-container">
                    <div className="custom-profile">
                        <div className="custom-profile-image">
                            {usuario.rutaPublicaciones && usuario.rutaPublicaciones[0] &&
                                renderProfileImage(usuario.rutaPublicaciones[0])}
                        </div>
                        <div className="custom-profile-user-settings">
                        <div className="custom-profile-user-settings2">
                            <h1 className="custom-profile-user-name">{usuario.nickname}</h1>
                                <button className="btn custom-profile-edit-btn" onClick={toggleContacts}>Mostrar Contactos</button>
                                <button className="btn custom-profile-edit-btn" onClick={toggleSensitiveData}>Datos Sensibles</button>
                        </div>
                                {showSensitiveData && (
                              <div className="sensitiveData">
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>Mail:</span> {usuario.mail}</p>
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>Año de nacimiento:</span> {usuario.dateBth}</p>
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>Session id:</span> {usuario.sessionid}</p>
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>Password:</span> {usuario.password}</p>
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>MFA:</span> {String(usuario.MFA)}</p>
                                <p style={{ fontSize: '12px' }}><span style={{ fontWeight: 'bold' }}>Codigo 2FA:</span> {usuario.number}</p>
                          </div>
                          
                                )}
                        </div>
                        <div className="custom-profile-stats">
                            <ul>
                                <li>
                                    <span className="custom-profile-stat-count">{usuario.postNum}</span> posts
                                </li>
                                <li onClick={toggleFollowers}>
                                    <span className="custom-profile-stat-count">{usuario.followersNum}</span> followers
                                </li>
                                <li onClick={toggleFollowing}>
                                    <span className="custom-profile-stat-count">{usuario.followingNum}</span> following
                                </li>
                            </ul>
                        </div>

                        <Modal isOpen={modalFollowers} toggle={() => setModalFollowers(!modalFollowers)} className="profile-modal">
                            <ModalHeader toggle={() => setModalFollowers(!modalFollowers)} className="profile-modal-header">Seguidores</ModalHeader>
                            <ModalBody className="profile-modal-body">
                                {followersList.map((follower, index) => (
                                    <div key={index} className="profile-modal-list-item">{follower}</div>
                                ))}
                            </ModalBody>
                        </Modal>

                        <Modal isOpen={modalFollowing} toggle={() => setModalFollowing(!modalFollowing)} className="profile-modal">
                            <ModalHeader toggle={() => setModalFollowing(!modalFollowing)} className="profile-modal-header">Siguiendo</ModalHeader>
                                <ModalBody className="profile-modal-body">
                                {followingList.map((following, index) => (
                                    <div key={index} className="profile-modal-list-item">{following}</div>
                                ))}
                            </ModalBody>
                        </Modal>

                        <Modal isOpen={modalContacts} toggle={() => setModalContacts (!modalContacts)} className="profile-modal">
                            <ModalHeader toggle={() => setModalContacts(!modalContacts)} className="profile-modal-header">Contactos</ModalHeader>
                            <ModalBody className="profile-modal-body">
                                {listaContactos.map((contacto, index) => (
                                <div 
                                    key={index} 
                                    className="profile-modal-list-item" 
                                    dangerouslySetInnerHTML={{ __html: procesarBiografia(contacto) }}
                                ></div>
                                ))}
                            </ModalBody>
                        </Modal>

                    
                        <div className="custom-profile-bio">
                            <p dangerouslySetInnerHTML={{ __html: procesarBiografia(usuario.Biografia) }}></p>
                        </div>
                    </div>
                </div>
                <button className="custom-open-sesion" onClick={handleOpenSession}>Abrir sesión</button>
            </header>
            <main>
                <div className="custom-container">
                    <div className="custom-gallery">
                        {usuario.rutaPublicaciones && Array.isArray(usuario.rutaPublicaciones) &&
                            usuario.rutaPublicaciones.map((ruta, index) => (
                                renderMedia(ruta, index)
                            ))}
                    </div>
                </div>
            </main>
            {modalOpen && (
                <div className="custom-modal">
                    <span className="custom-modal-close" onClick={closeModal}>&times;</span>
                    {renderModalContent()}
                   
                    <button className="custom-modal-prev" onClick={previousMedia}>&#8249;</button>
                    <button className="custom-modal-next"onClick={previousMedia}>&#8250;</button>
                </div>
            )}
        
        </div>
    );
}

export default PerfilUsuario;
