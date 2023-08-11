### Build and install packages
FROM python:3.9 as build-python

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

### Final image
FROM python:3.9-slim

RUN groupadd -r ora && useradd -r -g ora ora

RUN apt-get update \
  && apt-get install -y \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  liblcms2-2 \
  libopenjp2-7 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libssl1.1 \
  libtiff5 \
  libwebp6 \
  libxml2 \
  libpq5 \
  shared-mime-info \
  mime-support \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/media /app/static/images \
  && chown -R ora:ora /app/

COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app

ARG STATIC_URL
ENV TRUSTED_CORS_ORIGINS "http://localhost:3000,http://localhost"
ENV STATIC_URL ${STATIC_URL:-/static/}
ENV DEBUG 0
ENV ALLOWED_CLIENT_HOSTS "127.0.0.1,localhost,localhost:8000"
RUN SECRET_KEY=dummy STATIC_URL=${STATIC_URL} python3 manage.py collectstatic --no-input

EXPOSE 8000
ENV PYTHONUNBUFFERED 1

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PROJECT_VERSION="${PROJECT_VERSION}"

LABEL org.opencontainers.image.title="promptequation/oral-ehealth"                        \
      org.opencontainers.image.description="headless oral e-health framework,"            \
      org.opencontainers.image.url="https://www.promptequation.com/"                      \
      org.opencontainers.image.source="https://github.com/odoogap/oehealth"               \
      org.opencontainers.image.revision="$COMMIT_ID"                                      \
      org.opencontainers.image.version="$PROJECT_VERSION"                                 \
      org.opencontainers.image.authors="PROMPTEquation (https://www.promptequation.com)"  \
      org.opencontainers.image.licenses="BSD 3"

RUN python3 manage.py makemigrations
RUN python3 manage.py makemigrations api
RUN python3 manage.py makemigrations chat
RUN python3 manage.py makemigrations common
RUN python3 manage.py makemigrations appointment
RUN python3 manage.py makemigrations auth_extend
RUN python3 manage.py makemigrations notification

CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "backend.asgi:application"]
