const express = require("express")
const app = express()
const cors = require('cors');
const path = require('path')
const conection=require("./connection")
const nunjucks = require('nunjucks')
const bodyParser = require('body-parser');
const { User } = require("./models/models")

require("dotenv").config()

app.use(express.json())

const rutaRelativaImagenes = '../../../imagenes';
app.use('/TFG/imagenes', express.static(path.join(__dirname, rutaRelativaImagenes)));

app.use(cors({
   origin: process.env.IP
 }));

// CONEXIÓN BD - START

sequelize = conection

try {
   sequelize.authenticate();
   console.log('Connection has been established successfully.');
} catch (error) {
   console.error('Unable to connect to the database:', error);
}

// CONEXIÓN BD - END

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// CONFIG DE VISTAS - START
app.set('views', path.join(__dirname, 'views'))

nunjucks.configure('views', {
   autoescape: true,
   express: app
});


//var indexRouter = require('./routes/index')
//var authRouter = require('./routes/auth')
//app.use('/', indexRouter)
//app.use('/auth', authRouter)
// CONFIG DE VISTAS - END
app.use("/", require("./routes"))

const port = process.env.PORT

app.listen(port, () => console.log(`Server Started on port ${port}...`))
