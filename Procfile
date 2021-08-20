release: python manage.py migrate

web: bin/start-pgbouncer gunicorn tweet_tagger.wsgi:application --log-file=-