FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /sellor
RUN apk add build-base
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD ["sh", "sayhello.sh"]