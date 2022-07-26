FROM nginx:1.20.2

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /etc/nginx/nginx.conf.template

COPY run_nginx.sh /run_nginx.sh

RUN chmod +x /run_nginx.sh
