#!/bin/bash
set -e

echo "Деплой FEFU Lab $(date)"

PROJECT_DIR="/var/www/fefu_lab"
REPO_URL="https://github.com/Architect-byte/Django1.git"
DB_PASS="user"

if [[ $EUID -ne 0 ]]; then
    echo "Запуск от root: sudo $0"
    exit 1
fi

# Остановка сервисов
systemctl stop gunicorn nginx || true

# Решение lock проблем
#rm -f /var/lib/dpkg/lock* /var/cache/apt/archives/lock
#dpkg --configure -a

# Установка ПО
apt update
apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx git libpq-dev

# PostgreSQL
systemctl restart postgresql
sudo -u postgres psql -c "CREATE DATABASE fefu_lab_db;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER fefu_user WITH PASSWORD '$DB_PASS';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fefu_lab_db TO fefu_user;"

# Очистка и клонирование
rm -rf $PROJECT_DIR/project $PROJECT_DIR/deploy
mkdir -p $PROJECT_DIR/{deploy/{nginx,systemd,gunicorn,scripts},static,media}
cd $PROJECT_DIR
git clone $REPO_URL project

# Проект
cd project
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# БД и данные
python manage.py migrate --run-syncdb
python manage.py populate_db
python manage.py collectstatic --noinput

# Конфиги (копируются из репозитория или создаются)
sudo cp deploy/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
sudo cp deploy/nginx/fefu_lab.conf /etc/nginx/sites-available/fefu_lab.conf
sudo ln -sf /etc/nginx/sites-available/fefu_lab.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Права
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

# Сервисы
cp deploy/systemd/gunicorn.service /etc/systemd/system/
cp deploy/gunicorn/config.py $PROJECT_DIR/deploy/gunicorn/
cp deploy/nginx/fefu_lab.conf /etc/nginx/sites-available/
ln -sf /etc/nginx/sites-available/fefu_lab.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t && systemctl restart nginx
systemctl daemon-reload
systemctl start gunicorn && systemctl enable gunicorn

# Проверка
sleep 5
if curl -f http://localhost:80 >/dev/null 2>&1; then
    IP=$(hostname -I | awk '{print $1}')
    echo "УСПЕХ! Доступно: http://$IP"
    echo "Nginx: $(systemctl is-active nginx)"
    echo "Gunicorn: $(systemctl is-active gunicorn)"
else
    echo "Ошибка доступности"
    systemctl status gunicorn --no-pager
    exit 1
fi