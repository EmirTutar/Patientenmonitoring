Matix
==========
[Matrix Synapse Docker Hub](https://hub.docker.com/r/matrixdotorg/synapse)
Create a config file for your home server

```bash
docker run -it --rm \
    --mount ./data:data \
    -e SYNAPSE_SERVER_NAME=my.matrix.host \
    -e VIRTUAL_PORT: 8008 \
    -e SYNAPSE_REPORT_STATS: "no" \
    matrixdotorg/synapse:latest generate
```

Postgress 
=========

[Postgres](https://hub.docker.com/_/postgres)

Specify using postgress in homesever.yaml


Nginx Reverse Proxy
==================
The recumended way 
[Nginx](https://medium.com/@sncr28/deploying-a-matrix-server-with-element-chat-in-docker-compose-with-nginx-reverse-proxy-cc9850fd32f8)

Certbot
==========
First use the non cerrificate nginx_noncert.conf for nginx. The certify the your server.
In order to use HTTPS we need a valid TLS certificate. Certbot is an easy way to do this. [Certbot](https://mindsers.blog/en/post/https-using-nginx-certbot-docker/)
To test the setup use
```
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org
```
If everything succsseds, you can cerate the certificate by ussing:
```
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org
```
Certbot automatically renews your certificate once it is launches in the background.

Now we can use the real nginx.conf for nginx. 



Create user on homeserver
==========
```bash
 docker exec -it matrix_synapse register_new_matrix_user https://raspi4sysadmin.dynv6.net/ -c /data/homeserver.yaml --help
```
# Element
There are various clients for matirx a popular one ist [Element](https://element.io/)