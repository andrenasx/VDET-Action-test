FROM python:3.9-alpine3.17

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["ls", "-a"]
