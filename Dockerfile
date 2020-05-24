# pull official base image
FROM python:3.8.2-alpine
LABEL maintainer="pablohn6@gmail.com"


# set working directory
WORKDIR /usr/src/app

# add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy main files
COPY ./main.py /usr/src/app/main.py
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
