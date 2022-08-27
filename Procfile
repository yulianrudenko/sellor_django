release: python src/manage.py makemigrations && python src/manage.py migrate
web: cd src && daphne src.core.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python src/manage.py runworker --settings=core.settings_dir.production -v2