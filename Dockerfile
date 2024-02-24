FROM python:3.11
LABEL maintainer="tg @saniori"

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3.11", "main.py"]