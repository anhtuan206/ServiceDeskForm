FROM nginx:latest
RUN addgroup -S nonroot && adduser -S nonroot -G nonroot
USER nonroot
COPY ./ /etc/nginx/
