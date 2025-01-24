FROM python:3.11.10-alpine3.19
LABEL mantainer="jaopiovezam@gmail.com"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "djangoapp" e "scripts" para dentro do container.
COPY . .
#COPY ./scripts /scripts

# Entra na pasta djangoapp no container
WORKDIR /public

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev

RUN apk update && \
    apk upgrade && \
    apk --update add logrotate openssl bash && \
    apk add --no-cache certbot certbot-nginx

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN python -m venv /venv 
RUN /venv/bin/pip install --upgrade pip 
RUN  /venv/bin/pip install -r /public/requirements.txt 
RUN  adduser --disabled-password --no-create-home duser 
RUN  mkdir -p /public/data/web/static 
RUN  mkdir -p /public/data/web/media 
RUN  mkdir -p /public/data/web/static/admin 
RUN  chown -R duser:duser /public/venv 
RUN  chown -R duser:duser /public/data/web/static 
RUN  chown -R duser:duser /public/data/web/media 
RUN  chown -R duser:duser /public/data/web/static/admin 
RUN  chmod -R 755 /public/data/web/static 
RUN  chmod -R 755 /public/data/web/media 
RUN  chmod -R 755 /public/data/web/static/admin 
RUN  chmod -R +x /public/scripts

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/public/scripts:/venv/bin:$PATH"

# Muda o usuário para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]