FROM python:3.7.1
LABEL version="1.0.0"
LABEL description="This is a demo of the WAMP protocol."
LABEL url="https://github.com/alterway/wamp-polls"
LABEL author="Gilles Lenfant <gilles.lenfant@alterway.fr>"

EXPOSE 8080

WORKDIR /app
COPY .crossbar .crossbar
COPY manage.py .
COPY frozen-requirements.txt .
COPY apps apps
COPY project project
COPY static static
COPY templates templates

RUN find project -name '*.py[c|o]' -type 'f' -delete && \
    find project -name '__pycache__' -type 'd' -delete && \
    pip install --no-cache-dir -r frozen-requirements.txt && \
    mkdir -p var/db var/log var/static && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mydomain.com', 'admin')" && \
    find . -name "tests" -type "d" -delete

CMD ["crossbar", "start"]
