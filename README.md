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

`pip3 install --upgrade googlemaps --break-system-packages`

`pip3 install --upgrade brazilcep --break-system-packages`

`pip3 install --upgrade python-dotenv --break-system-packages`

`pip3 install --upgrade pytest-django --break-system-packages`

`pip3 install --upgrade pytest-cov --break-system-packages`

`pip3 install --upgrade coverage --break-system-packages`

#`pip3 install --upgrade pytest-cov --break-system-packages`


### Comandos de inicialização do projeto:

`pip3 freeze`

`django-admin startproject univesp_pi_2`

`mv univesp_pi_2 univesp-pi-2 && cd univesp-pi-2`

`django-admin startapp combate_aedes`

### Comandos para execução do projeto localmente:

`cd univesp-pi-2`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py collectstatic --noinput --clear`

`python3 manage.py runserver 0.0.0.0:8000`

### Comandos para recriar o banco:

`cd univesp-pi-2`

`find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`

`find . -path "*/migrations/*.pyc" -delete`

`find . -path "*/db.sqlite3" -delete`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

### Comandos para criar banco de dados na plataforma Heroku:

`heroku login`

`heroku run python manage.py makemigrations --app combate-aedes`

`heroku run python manage.py migrate --app combate-aedes`

### Comandos de debug na Heroku:

`heroku logs --tail --app combate-aedes`

### Comandos de teste:

`cd univesp-pi-2`

`coverage erase`

`coverage run -m pytest tests`

`coverage report`

`coverage html`

`pytest --cov`

`pytest --cov-report html --cov`

`python3 manage.py test`