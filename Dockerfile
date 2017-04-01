FROM python:2
MAINTAINER "zzzzzzj <support@mail.zzzzzzj.me>"

ENV API_KEY="YOUR-API-KEY" \
	API_PASS="YOU-API-PASSWORD" \
	CONTAINER="YOU-CONTAINER-ID" \
	INTERVAL="300"
	
COPY ./requirement.txt /app/requirement.txt

RUN pip install -r /app/requirement.txt

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y wget libpcre3-dev build-essential libssl-dev cron && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget http://nginx.org/download/nginx-1.11.2.tar.gz && \
    tar -zxvf nginx-1.*.tar.gz && \
    cd nginx-1.* && \
    ./configure \
		--prefix=/opt/nginx \
		--user=nginx \
		--group=nginx \
		--with-http_ssl_module \
		--with-ipv6 \
		--with-threads \
		--with-stream \
		--with-stream_ssl_module && \
    make && make install && \
    cd .. && rm -rf nginx-1.*

RUN adduser --system --no-create-home --disabled-login --disabled-password --group nginx

RUN ln -sf /dev/stdout /opt/nginx/logs/access.log \
	&& ln -sf /dev/stderr /opt/nginx/logs/error.log \
	&& touch /opt/nginx/conf/sakura.conf

WORKDIR /

COPY ./getserver.py /app/getserver.py

COPY ./nginx.conf /opt/nginx/conf/nginx.conf

EXPOSE 	11223

CMD /opt/nginx/sbin/nginx && python /app/getserver.py --api-key $API_KEY --api-pass $API_PASS --container-id $CONTAINER --interval $INTERVAL