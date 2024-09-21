# univesp-pi-2

## UNIVESP, 2024

Projeto Integrador em Computação II - Grupo 15

### Comandos de instalação do python3:

`brew upgrade && brew update && brew install python3 && brew cleanup phyton3 && python3 --version`

### Comandos de instalação do django e demais componentes:

`pip3 install --upgrade pip --break-system-packages`

`pip3 install --upgrade Django --break-system-packages`

`pip3 install --upgrade whitenoise --break-system-packages`

`pip3 install --upgrade dj-database-url --break-system-packages`

`pip3 install --upgrade django-heroku --break-system-packages`

### Comandos de inicialização do projeto:

`django-admin startproject univesp_pi_2`

`mv univesp_pi_2 univesp-pi-2 && cd univesp-pi-2`

`django-admin startapp combate_aedes`

### Comandos para execução do projeto localmente:

`cd univesp-pi-2`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py collectstatic --noinput --clear`

`python3 manage.py runserver 0.0.0.0:8000`

### Comandos de debug na Heroku:

`heroku logs --tail --app combate-aedes`