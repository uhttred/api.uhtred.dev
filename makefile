HOST := localhost
PORT := 8000
user :=
ctx :=

# === SERVING

serve:
	@./manage.py runserver ${HOST}:${PORT}

docup: # docker-compose up
	# docker compose up services in -d mode
	@docker-compose up -d --build
	# waiting database
	@sleep 5
	# sync database
	@docker-compose run api make dbsync
	# start logging
	@docker-compose logs -f

up:
	@docker-compose up

down:
	@docker-compose down

# === INSTALATIONS

install:
	# instaling production dependencies
	@pip install --no-cache-dir -r requirements.txt

install-dev:
	# instaling local dependencies for development
	@pip install -r requirements/local.txt

env-export:
	# exporting env vars in .env file to bash
	@export $(grep -v '^#' .env | xargs -d '\n')

test:
	# ---------------------- Testing All Apllication ---------------------
	@python manage.py test \
		--pattern="test_*.py" \
		--keepdb --verbosity 1 \
		--failfast \
		--force-color

# === DATABASE

migrations:
	@python manage.py makemigrations
migrate:
	@python manage.py migrate
dbsync:
	# applying migrations
	@python manage.py makemigrations
	# migrate
	@python manage.py migrate

# === SCRIPTS AND COMMANDS

messages:
	# making messages for translations
	@python manage.py makemessages -l pt

compilemessages:
	@django-admin compilemessages
	
shell:
	@python manage.py shell
check:
	@python manage.py check
