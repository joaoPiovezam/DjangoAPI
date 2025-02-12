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
RUN mkdir /app

WORKDIR /app

COPY . /app
COPY scripts /scripts

# Entra na pasta djangoapp no container


# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN python -m venv /venv 
RUN  /venv/bin/pip install --upgrade pip 
RUN  /venv/bin/pip install -r requirements.txt 
RUN  adduser --disabled-password --no-create-home duser 
RUN  mkdir -p /data/web/static 
RUN  mkdir -p /data/web/media 
RUN  chown -R duser:duser /venv 
RUN  chown -R duser:duser /data/web/static 
RUN  chown -R duser:duser /data/web/media 
RUN  chmod -R 755 /data/web/static 
RUN chmod -R 755 /data/web/media 
RUN  chmod -R +x /scripts 
RUN chmod -R 755 ../etc/letsencrypt/live/api.athlan.com.br/


RUN chmod +x  commands.sh

ENV PATH="/scripts:/venv/bin:$PATH"
  # Start the application using Gunicorn
#CMD  ["./commands.sh"]
#CMD  ["python",  "manage.py", "runserver", "0.0.0.0:80"]
CMD   ["python",  "manage.py", "runsslserver", "0.0.0.0:80",  "--certificate", "../etc/letsencrypt/live/api.athlan.com.br/fullchain.pem",  "--key", "../etc/letsencrypt/live/api.athlan.com.br/privkey.pem"]
