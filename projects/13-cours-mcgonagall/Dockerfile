# Dockerfile pour Electron + React + Vite
FROM node:20-bullseye

# Dépendances système pour Electron
RUN apt-get update && apt-get install -y \
    libgtk-3-0 libnss3 libxss1 libasound2 libxtst6 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxkbfile1 libsecret-1-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package*.json ./
COPY .eslintrc.json ./

RUN npm install

COPY . .

# Build l'app (Vite)
RUN npm run build

# Commande par défaut : test
CMD ["npm", "test"]

# Pour lancer en prod :
# docker run --rm -e NODE_ENV=production my-app npm start
