FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update && apt install -y libmariadb-dev
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .
