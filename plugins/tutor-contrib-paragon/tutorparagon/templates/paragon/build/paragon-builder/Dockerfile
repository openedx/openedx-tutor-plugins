FROM node:20-alpine

WORKDIR /paragon-builder

COPY entrypoint.sh ./entrypoint.sh
COPY package*.json ./

RUN npm ci && \
    chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]

CMD []
