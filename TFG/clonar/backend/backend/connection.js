require("dotenv").config()
const { Sequelize, DataTypes } = require("sequelize");

const DB_HOST = process.env.DB_HOST
const DB_USER = process.env.DB_USER
const DB_PASSWORD = process.env.DB_PASSWORD
const DB_DATABASE = process.env.DB_DATABASE
const DB_PORT = process.env.DB_PORT

const db = new Sequelize(DB_DATABASE, DB_USER, DB_PASSWORD, {
   host: DB_HOST,
   dialect: 'mysql',
   charset: 'utf8mb4', // Establece el conjunto de caracteres como utf8mb4
   collate: 'utf8mb4_unicode_ci'
});

module.exports=db;