# Microservicio: Middleware Discord/Telegram

* Javier Jaure 202004544-5
* Danny Fuentes 201773559-7
* Bastian Varas 201856629-2

# Ejecucion del programa

Para ejecutar el demo, se debe ejecutar ```docker compose up``` lo cual iniciara la api en el puerto
localhost:5000. Ejecutara ademas, Rabbitmq con el managment en el puerto localhost:15672.

La app consiste en que por medio de un chatbot de Discord/telegram se enviaran el dato de los mensajes 
a los endpoint de la API, la cual a su vez enviara eventos a la cola rabbitmq y escuchara eventos de la cola rabbitmq.

## Variables de entorno
se deben settear las siguientes variables de entorno
```
DISCORD_TOKEN: Token del bot de discord
USER_HOST="http://middleware:80" # esta variable es para la conexión con el servicio de usuarios. Pero para efectos de prueba, nosotros mockeamos las posibles respuestas.
```