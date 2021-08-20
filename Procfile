release: python manage.py migrate

web: gunicorn tweet_tagger.wsgi:application --log-file=-