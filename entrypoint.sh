#!/bin/sh
set -e

# Espera pelo banco de dados (PostgreSQL ou MySQL)
echo "Aguardando o banco de dados em $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "Banco de dados disponível!"

# Aplica migrações
echo "Aplicando migrações..."
python manage.py migrate --noinput

# Coleta arquivos estáticos (caso tenha sido removido do Dockerfile)
# python manage.py collectstatic --noinput

# Cria superusuário automaticamente se desejado
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "Criando superusuário..."
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME}',
        email='${DJANGO_SUPERUSER_EMAIL}',
        password='${DJANGO_SUPERUSER_PASSWORD}'
    )
END
fi

# Inicia o servidor Django (ou troque por Gunicorn)
echo "Iniciando o servidor..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000