# Deploy Guide

- Ubuntu 18.04.5 LTS
- nginx/1.14.0
- Python 3.6.9
- pip 9.0.1

---
## IMPORTANT

### *以下内容没有经过测试验证，所以都是我瞎扯的*

## Install Nginx

```bash
sudo apt update
sudo apt upgrade
```
我也不知道上面两个的具体功能，`apt` 报错用就完了。

```bash
sudo apt install nginx
```

## Install Python and pip

```bash
sudo apt install python3
sudo apt install python3-pip
```

## Install package

```bash
pip3 install uwsgi
pip3 install -r requirement.txt
```

可能会报错？ 你问我我也不知道。

```bash
python3 manage.py runserver
```
看看缺什么就安什么啦。（以上命令开启的是测试服务器，性能感人）

## Nginx Config

```
/etc/nginx/sites-enabled
```

```
upstream django {
    server 127.0.0.1:8001; 
}
server {
    listen      80;
    server_name mpserver.umeh.top;
    charset     utf-8;

    location / {
        uwsgi_pass  django;
        include     /home/admin/server/uwsgi_params; # the uwsgi_params file you installed
    }
}

server {
    listen 443;
    ssl on;
    server_name mpserver.umeh.top;
    ssl_certificate  /var/cert/cert.crt;   
    ssl_certificate_key /var/cert/private.key;  
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    location / {
	uwsgi_pass  django;
        include     /home/admin/server/uwsgi_params; # the uwsgi_params file you installed
    }
}

server{
	listen 443;
	ssl on;
	server_name umeh.top www.umeh.top;
	ssl_certificate /var/cert/umeh.top/cert.crt;
	ssl_certificate_key /var/cert/umeh.top/private.key;
	ssl_session_timeout 5m;
	ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	ssl_prefer_server_ciphers on;
	location / {
		root /home/admin/website;
		index index.html;
	}
 	rewrite  ^/reviews/(.*)/(.*)$ /reviews.html?course=$1&instructor=$2 last;
	rewrite  ^/instructor/(.*)$ /search.html?keyword=$1&instructor=true last;
	rewrite  ^/professor/(.*)$ /search.html?keyword=$1&instructor=true last;
	rewrite  ^/course/(.*)$ /course.html?course=$1&instructor=$2 last;
}
upstream real_ga_servers {
        server www.google-analytics.com:443 weight=5 max_fails=0;
        keepalive 64;
}

server {    
   listen 443 ssl;
   server_name ga.umeh.top;
   
   ssl on;
   ssl_certificate  /var/cert/ga.umeh.top/cert.crt;
    ssl_certificate_key /var/cert/ga.umeh.top/private.key;
    ssl_session_timeout 5m;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;


    location / {

        rewrite ^(.*)$   $1?uip=$remote_addr    break;
    
        proxy_set_header   Host       www.google-analytics.com;

        # Proxy to google-analytics.com
         proxy_buffering off;

         proxy_http_version 1.1; # require  nginx > 1.1.4
         proxy_set_header Connection ""; # for keepalive upstream

         proxy_pass https://real_ga_servers ;
         proxy_redirect off;

    }
}
server{
	listen	80;
	server_name www.umeh.top umeh.top;
	location / {
		root /home/admin/website;
		index index.html index.htm index.php;
	}
	 return      301 https://$server_name$request_uri; 
}
server{
	listen 80;
	server_name web.umeh.top;

}
```

```bash
nginx -t
sudo systemctl restart nginx
```

## Launch

```
uwsgi --socket :8001 --module server.wsgi
```



## Reference
[Setting up Django and your web server with uWSGI and nginx](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)
