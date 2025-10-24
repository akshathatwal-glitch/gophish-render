#!/bin/sh
envsubst '${PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
/app/gophish &
nginx -g 'daemon off;'