docker-compose:
	#docker-compose -f ./docker/local/docker-compose.yaml --env-file .env up --build -d
	docker-compose --project-name artfoot_local -f ./docker/local/docker-compose.yaml --env-file .env up --build -d

makemigrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

translations:
	python3 manage.py update_translation_fields

locale_file_ru:
	python3 manage.py makemessages -l ru -i venv
locale_file_kz:
	python3 manage.py makemessages -l kk -i venv

compilemessages:
	python3 manage.py compilemessages --ignore=venv


start:
	 gunicorn config.wsgi:application -w 4 -b 0.0.0.0:8083

celery_task_clear_old_cart:
	celery -A config worker --detach

celery_beat_clear_old_cart:
	celery -A config beat --detach