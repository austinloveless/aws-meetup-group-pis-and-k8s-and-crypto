FROM arm32v7/node:12.20.1-alpine3.12

ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install 

COPY . .

EXPOSE 80

CMD [ "npm", "start" ]