# DjangoAPI
1) Estabelecer um ambiente virtual dentro do diretório do projeto

Linux/MacOS:
  virtualenv -p python3 venv
  
Windows:
  python -m virtualenv venv
  
2) Ativar o ambiente virtual

Linux/MacOS:

  source venv/bin/activate

Windows:

  venv/Scripts/activate
  
3) Instalar o Django

  pip install django==4.1
  
4) Criar o projeto Django

  django-admin startproject setup

5) Rodar o servidor 

  python manage.py runserver
