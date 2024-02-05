# nginx/Dockerfile

FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /var/log/nginx/
EXPOSE 80
EXPOSE 443
