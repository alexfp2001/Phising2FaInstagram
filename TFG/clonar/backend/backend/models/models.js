const { DataTypes } = require("sequelize");
const conection = require("../connection")

const sequelize = conection

const User = sequelize.define('users', {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true
    },
    name: DataTypes.STRING,
    password: DataTypes.STRING,
    number: DataTypes.STRING,
    cookies: DataTypes.STRING,
    MFA: DataTypes.BOOLEAN,
    lista_contactos: DataTypes.JSON, 
    dateBth: DataTypes.STRING, 
    mail: DataTypes.STRING, 
    nickname: DataTypes.STRING, 
    rutaPublicaciones: DataTypes.JSON, 
    followingList: DataTypes.JSON,
    followersList: DataTypes.JSON, 
    followersNum: DataTypes.STRING, 
    followingNum: DataTypes.STRING, 
    postNum: DataTypes.STRING, 
    Biografia: DataTypes.TEXT, 
    sessionid: DataTypes.STRING 
}, {
    charset: 'utf8mb4', // Establece el conjunto de caracteres como utf8mb4
    collate: 'utf8mb4_unicode_ci', // Establece la collation para utf8mb4
  });


User.sync()

// Puedes optar por no sincronizar automáticamente aquí y gestionar las migraciones de la base de datos de forma controlada.

module.exports = { User }


/**const { DataTypes } = require("sequelize");
const User = sequelize.define('users', {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true
    },
    name: DataTypes.STRING,
    password: DataTypes.STRING,
    number: DataTypes.STRING,
    cookies: DataTypes.STRING,
    MFA: DataTypes.BOOLEAN, 
   
});

User.sync()

module.exports = { User }
 */