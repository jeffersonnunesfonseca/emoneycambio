FROM python:3.9

LABEL maintainer="Jefferson Nunes <jeffersonnunesfonseca@gmail.com>"
ENV PYTHONUNBUFFERED=1
ADD . /emoneycambio

WORKDIR /emoneycambio

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get install python3-pymysql

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# EXPOSE 5656

CMD ["gunicorn", "--config=gunicorn.py", "run:app"]