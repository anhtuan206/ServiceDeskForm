FROM python:alpine
RUN apk add --no-cache gcc
RUN apk add --no-cache curl
RUN pip install --upgrade pip
COPY  . /code
WORKDIR /code
RUN mkdir /code/logs
RUN chmod +x gunicorn.sh
RUN pip install -r requirements.txt
EXPOSE 51806
ENTRYPOINT ["./gunicorn.sh"]
# ENTRYPOINT ["python","app.py"]