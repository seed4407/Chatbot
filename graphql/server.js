var express = require("express")
var { graphqlHTTP } = require("express-graphql")
var { buildSchema } = require("graphql")
var axios = require('axios');
const cors = require('cors');

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`
  type Query {
    perfil(id: String): [String]
    loging(username: String, password: String): String
    info_plantas: [[String]]
  }

  type Mutation {
    creacion_usuario(name: String,username: String, password: String,email: String, phone_number: Int): String
  }

  type Usuario {
    name: String,
    username: String,
    password: String,
    email: String,
    admin: Boolean,
    phone_number: Int,
    token: String
  }
`)

// The root provides a resolver function for each API endpoint
var root = {
  hello: () => {
    return "Hello world!"
  },
  perfil: async ({id}) => {
    try {
      const response = await axios.get('http://tarea_u4_service_users/users/'+id);
      let datos = [response.data["name"], response.data["username"], response.data["email"], String(response.data["phone_number"])];
      console.log(datos);
      return datos;
    } catch (error) {
      console.error(error);
      return [];
    }
  },
  loging: async ({username,password}) => {
    try {
      const response = await axios.get('http://tarea_u4_service_users/users/'+username+'/'+password);
      console.log(response.data)
      if(response.data[0] === "No se encontro usuario" || response.data[0] === "Contraseña Incorrecta"){
        return "Ingreso mal usuario/contrasena"
      } 
      else{
        return "Ok";
      }
    } catch (error) {
      console.error(error);
      return "Ingreso mal usuario/contrasena";
    }
  },

  //No funciona, arreglar despues. Ademas deberia crear en conjunto usuario con granja
  creacion_usuario: (name,username,password,email,phone_number) => {
      console.log("entra");
      let usuario = {
        "name": name,
        "username": username,
        "password": password,
        "email": email,
        "admin": true,
        "phone_number": phone_number,
        "token": "1234567890abcdef"
      };
      try{
        fetch('http://tarea_u4_service_users/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: usuario
        })
        .then(r => r.json())
        .then(data => console.log('data returned:', data));
        console.log("sale");
        return "Ok"
      } catch (error) {
        console.error(error);
        return "Ingreso mal usuario/contrasena";
      }
  },

  info_plantas: async ({}) => {
    const response = await axios.get('http://granja_service/plants');
    let lista = [];
    for(i = 0;i<response.data.length;i++){
      lista.push([response.data[i]["name"],response.data[i]["daysToGrow"],response.data[i]["lifeExpectancy"],response.data[i]["minHarvest"],response.data[i]["maxHarvest"],response.data[i]["description"]]);
    }
    return lista;
    
  },
}

var app = express()
app.use(cors({
  origin: 'http://localhost:3000'  // reemplaza esto con tu dominio
}));
app.use(
  "/graphql",
  graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true,
  })
)
app.listen(4000)
console.log("Running a GraphQL API server at http://localhost:4000/graphql")