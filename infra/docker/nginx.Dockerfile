FROM node:24-bookworm-slim AS web-build

WORKDIR /app/apps/web

COPY apps/web/package.json /app/apps/web/package.json
COPY apps/web/package-lock.json /app/apps/web/package-lock.json
RUN npm ci

COPY apps/web /app/apps/web
RUN npm run build

FROM nginx:1.29.6-alpine3.23-slim

COPY infra/nginx/default.conf /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=web-build /app/apps/web/dist/web/browser/ /usr/share/nginx/html/
