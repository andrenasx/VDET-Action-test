FROM python:3.9-slim-bullseye

COPY . /vdet

ENTRYPOINT ["/vdet/entrypoint.sh"]