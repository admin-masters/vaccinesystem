#!/bin/bash
set -e

echo "🚀 Starting Vaccine System Deployment..."

APP_DIR="/var/www/vaccine"
VENV_DIR="/var/www/venv"
ENV_FILE="/var/www/secrets/.env"

echo "📂 Moving to app directory"
cd $APP_DIR

echo "🔄 Pulling latest code from GitHub"
git pull origin main

echo "🐍 Activating virtual environment"
source $VENV_DIR/bin/activate

echo "📦 Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "🌱 Loading environment variables"
export $(grep -v '^#' $ENV_FILE | xargs)

echo "🗄️ Running migrations"
python manage.py migrate --noinput

echo "🎨 Collecting static files"
python manage.py collectstatic --noinput

echo "🔁 Restarting Gunicorn"
sudo systemctl restart gunicorn-vaccine

echo "✅ Deployment completed successfully!"
