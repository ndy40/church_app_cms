FROM python:3.10.4-alpine3.15 AS basestage
RUN apk add --update-cache \
    gcc \
    postgresql-client \
    libpq-dev \
    git
RUN python -m pip install --upgrade pip


FROM basestage AS devstage
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=${APP_ENV:-dev}
WORKDIR /opt/app/
COPY infrastructure/start_server.sh requirements* /opt/app/
COPY church_cms/ /opt/app/church_cms/

RUN python -m venv venv; \
    source venv/bin/activate; \
    python -m pip install -r requirements_dev.txt

WORKDIR /opt/app/church_cms

EXPOSE 8000
CMD ["/opt/app/start_server.sh"]
