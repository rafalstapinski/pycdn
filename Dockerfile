FROM python:3.10.7-buster

WORKDIR /app

COPY . /app

RUN cd /app
RUN pip install -r requirements.txt
ENV PYTHONPATH=.

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
