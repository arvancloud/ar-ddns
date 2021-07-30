from ubuntu:20.04

RUN apt update && \
    apt install -y jq && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ddns.sh .

ENTRYPOINT ["bash", "./ddns.sh"]
