FROM node:18-alpine

COPY entrypoint.sh /entrypoint.sh

RUN npm install --save @openedx/paragon && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]

CMD []
