FROM node:22-alpine

COPY entrypoint.sh /entrypoint.sh

WORKDIR /paragon-builder

RUN npm install --save @openedx/paragon && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]

CMD []
