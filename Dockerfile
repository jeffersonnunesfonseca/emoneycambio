FROM python:3.9

LABEL maintainer="Jefferson Nunes <jeffersonnunesfonseca@gmail.com>"
ENV PYTHONUNBUFFERED=1

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:br
ENV LC_ALL pt_BR.UTF-8
ENV TZ America/Sao_Paulo


ADD . /emoneycambio

WORKDIR /emoneycambio

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

VOLUME /run/secrets/env_vars

# COPY ./docker-entrypoint.sh /
# RUN chmod +x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

# EXPOSE 5656

CMD ["gunicorn", "--config=gunicorn.py", "-w 1","run:app"]