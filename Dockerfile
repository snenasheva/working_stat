FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["python", "run.py"]
