FROM python:3.10

WORKDIR /app

COPY  requirements.txt .

COPY main.py .

COPY config .
COPY config/__init__.py  /app/config/


RUN pip install -r requirements.txt

CMD [ "python","uvicorn","main:app","--host","0.0.0.0"."--port","8000" ]