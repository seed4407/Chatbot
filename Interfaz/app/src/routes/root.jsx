import React from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';
// import Link from 'react-bootstrap/Link';
import { Link } from 'react-router-dom';
import axios from 'axios';

import {
  Box,
  Text,
  // Link,
  Heading,
  Container,
  // Button,
  Stack,
  // Icon,
  // useColorModeValue,
  createIcon,
  Highlight,
} from '@chakra-ui/react';

import { Layout } from '../layout/Layout';

function eniar_mensaje() {
  if(document.getElementById("mensaje").value.toString() === "Catalogo de plantas"){
    axios.post('http://localhost:4000/graphql', {
      query: '{info_plantas}'
    })
    .then(res => {
      mensajeria(res["data"]["data"]["info_plantas"])
    })
    .catch(error => {
      console.error(error)}
    );
  }
}

function mensajeria(datos){
  let largo_lista = datos.length
  let variable = "";
  let dato;
  let contador = 0;
  while(contador<largo_lista){
    dato = datos[contador]
    variable = "<div>"+variable+"<p> Nombre: "+dato[0]+"</p><p>Descripcion: "+ dato[5]+"</p></div>";
    contador = contador +1;
  }
  var chat = document.getElementById("chat");
  chat.innerHTML = variable;
  console.log("%c" + variable, "color: black;");
}

export function Landing() {
  return (
    <>
      <Container maxW={'3xl'}>
        <Stack
          as={Box}
          textAlign={'center'}
          spacing={{ base: 8, md: 14 }}
          py={{ base: 20, md: 36 }}
        >
          <Heading
            fontWeight={600}
            fontSize={{ base: '2xl', sm: '4xl', md: '6xl' }}
            lineHeight={'0%'}
          >
            <Highlight
              query={['microservicios']}
              styles={{ px: '2', py: '0', rounded: 'full', bg: 'teal.100' }}
            >
              Chat
            </Highlight>
          </Heading>
          <Text color={'gray.500'}>
          <Card style={{ width: '130%', height: '200%'}}>
                <Card.Body>
                  <Card.Subtitle className="mb-2 text-muted"></Card.Subtitle>
                  <Card.Text>
                  </Card.Text>
                  <div class="container">
                    <div class="row">
                      <div class="col">
                        <Card style={{ width: '55rem', height: '300px',overflowY:'scroll'}}>
                          <Card.Body>
                            <Card.Title></Card.Title>
                            <Card.Subtitle className="mb-2 text-muted"></Card.Subtitle>
                            <Card.Text>
                              <p id='chat'></p>
                            </Card.Text>
                          </Card.Body>
                        </Card>
                      </div>
                      <div class="w-100"></div>
                      <div class="col">
                        <input type="text" placeholder="Escribe aquí" id='mensaje' style={{ width: '55rem',borderRadius: '8px',marginTop: '7px',paddingLeft:'7px'}}/>
                        <button style={{borderRadius: '10px', marginTop: '4px', marginLeft:'2px'}} onClick={eniar_mensaje}>Enviar</button>
                      </div>
                    </div>
                  </div>
                </Card.Body>
              </Card>
          </Text>
        </Stack>
      </Container>
    </>
  );
}

const Arrow = createIcon({
  displayName: 'Arrow',
  viewBox: '0 0 72 24',
  path: (
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M0.600904 7.08166C0.764293 6.8879 1.01492 6.79004 1.26654 6.82177C2.83216 7.01918 5.20326 7.24581 7.54543 7.23964C9.92491 7.23338 12.1351 6.98464 13.4704 6.32142C13.84 6.13785 14.2885 6.28805 14.4722 6.65692C14.6559 7.02578 14.5052 7.47362 14.1356 7.6572C12.4625 8.48822 9.94063 8.72541 7.54852 8.7317C5.67514 8.73663 3.79547 8.5985 2.29921 8.44247C2.80955 9.59638 3.50943 10.6396 4.24665 11.7384C4.39435 11.9585 4.54354 12.1809 4.69301 12.4068C5.79543 14.0733 6.88128 15.8995 7.1179 18.2636C7.15893 18.6735 6.85928 19.0393 6.4486 19.0805C6.03792 19.1217 5.67174 18.8227 5.6307 18.4128C5.43271 16.4346 4.52957 14.868 3.4457 13.2296C3.3058 13.0181 3.16221 12.8046 3.01684 12.5885C2.05899 11.1646 1.02372 9.62564 0.457909 7.78069C0.383671 7.53862 0.437515 7.27541 0.600904 7.08166ZM5.52039 10.2248C5.77662 9.90161 6.24663 9.84687 6.57018 10.1025C16.4834 17.9344 29.9158 22.4064 42.0781 21.4773C54.1988 20.5514 65.0339 14.2748 69.9746 0.584299C70.1145 0.196597 70.5427 -0.0046455 70.931 0.134813C71.3193 0.274276 71.5206 0.70162 71.3807 1.08932C66.2105 15.4159 54.8056 22.0014 42.1913 22.965C29.6185 23.9254 15.8207 19.3142 5.64226 11.2727C5.31871 11.0171 5.26415 10.5479 5.52039 10.2248Z"
      fill="currentColor"
    />
  ),
});

function App() {
  return (
    <Layout>
      <Landing />
    </Layout>
  );
}

export default App;
