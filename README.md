# DjangoAPI
1) Instalar pacotes necessario
  pip install -r requirements.txt

2) Estabelecer um ambiente virtual dentro do diretório do projeto

Linux/MacOS:

  virtualenv -p python3 venv
  
Windows:

  python -m virtualenv venv
  
3) Ativar o ambiente virtual

Linux/MacOS:

  source venv/bin/activate

Windows:

  venv/Scripts/activate
  
4) Instalar o Django

  pip install django==4.1
  
5) Criar o projeto Django

  django-admin startproject setup

6) Instalar rest framework

  pip install djangorestframework
  pip install markdown

7) Rodar o servidor 

  python manage.py runserver
