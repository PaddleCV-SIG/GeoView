FROM node:20.10.0-alpine
RUN mkdir /app
COPY frontend /app/frontend
WORKDIR /app/frontend
RUN npm install
ENTRYPOINT ["npm", "run", "serve"]
