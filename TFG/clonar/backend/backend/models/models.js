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
   
});

User.sync()

// Puedes optar por no sincronizar automáticamente aquí y gestionar las migraciones de la base de datos de forma controlada.

module.exports = { User }
