var express = require("express")
var { graphqlHTTP } = require("express-graphql")
var { buildSchema } = require("graphql")
var axios = require('axios');

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`
  type Query {
    perfil(id: String): [String]
    logging(name: String, password: String): String
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
  logging: async ({username,password}) => {
    try {
      const response = await axios.get('http://tarea_u4_service_users/users/'+username+'/'+password);
      let datos = response.data;
      console.log(datos);
      return "Ok";
    } catch (error) {
      console.error(error);
      return "Ingreso mal usuario/contrasena";
    }
  },
}

var app = express()
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