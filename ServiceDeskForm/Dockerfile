FROM python:alpine
ARG port=51813
# Chạy container với quyền root
# USER root
RUN apk add --no-cache gcc
RUN apk add --no-cache curl
RUN pip install --upgrade pip
COPY  ./ServiceDeskForm/ /code
# COPY  . /code
WORKDIR /code
RUN mkdir /code/logs
RUN chmod +x gunicorn.sh
RUN pwd
RUN ls
RUN pip install -r ./requirements.txt
EXPOSE ${port}
ENTRYPOINT ["./gunicorn.sh"]
# ENTRYPOINT ["python","app.py"]