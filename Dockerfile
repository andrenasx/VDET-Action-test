FROM python:3.9-slim-bullseye

COPY requirements.txt /vdet/requirements.txt

RUN cd /vdet && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /vdet

ENTRYPOINT ["/vdet/entrypoint.sh"]