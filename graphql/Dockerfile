FROM node:alpine

WORKDIR /code

COPY ./ ./

RUN ls

# RUN npm init
RUN npm i
RUN npm install -g express
RUN npm install graphql --save
RUN npm install -g axios

# RUN npm install apollo-server-express graphql @graphql-tools/schema --save
RUN npm install -g npm@10.2.3



CMD ["node", "server.js"]

