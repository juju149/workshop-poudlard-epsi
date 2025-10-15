FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

ENV PORT=3000
ENV DB_PATH=/data/hogwarts.db

RUN mkdir -p /data

CMD ["npm", "start"]
