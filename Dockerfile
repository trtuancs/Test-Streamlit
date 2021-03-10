FROM python:3.8.5

EXPOSE 8501

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .