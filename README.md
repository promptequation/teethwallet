# OeHMP - Oral e-Health Monitoring Platform
<img title="Oral e-Health Monitoring Platform" src="/OeHMP_logo.jpg">

## How to develop • Vue.js/Nuxt.js Frontend

• 16 Mar 2022 •••

1. Install Docker-compose (1.29.00 works)

2. Go to the 'oehmp' folder and run containers:

```bash
cp backend/db.sqlite3_empty backend/db.sqlite3
cp env.dev.localhost env.dev
docker-compose -f dev.yml --env-file env.dev up
```

3. Run the shell in Api container . This shell is bash terminal for django backend controll

```bash
docker-compose -f dev.yml exec api /bin/bash
```

and then inside the shell init database and fill it with testdata:

```bash
python manage.py makemigrations
python manage.py makemigrations api
python manage.py makemigrations chat
python manage.py makemigrations common
python manage.py makemigrations appointment
python manage.py makemigrations auth_extend
python manage.py migrate
python manage.py sample
```

4. The Django admin is available at `localhost:8080/admin_b/` after the restart.
   Google Chrome may not work correctly in Django Admin, try to use Opera or another browser.

5. The Vue.js/Nuxt frontend is available at `localhost:3000` after a few minutes, (when the Nuxt server would be compiled)

6. Use this commands:

```bash
docker-compose -f dev.yml logs -f api
docker-compose -f dev.yml logs -f frontend
```

for `api` and `frontend` containers resp. to see logs and debug the application

## Install

--

### Using docker-compose

```bash
docker-compose up -d
docker exec -it oehealth_api_1 python manage.py migrate
docker exec -it oehealth_api_1 python manage.py createsuperuser --username=dd --email=dd@dd.pt
(enter password twice)

navigate to:
- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/graphql

```

#### Frontend developers can just start the backend

```bash
docker-compose up --build api worker
```

### Backend developers can just start the frontend

```bash
docker-compose up --build frontend
```

## Production

```bash
# Everybody up
docker-compose -f docker-compose-staging.yml up -d
# Just trigger certbot
docker-compose -f docker-compose-staging.yml run certbot -it certonly --webroot \
                --webroot-path=/var/www/html --email support@odoogap.com --agree-tos \
                --no-eff-email --staging -n  -d oehealth.promptequation.com
```

## Seeding Data

```bash

docker exec -it oral-e-health_api_1 python manage.py loaddata /app/demo_data.json
