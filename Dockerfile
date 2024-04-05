FROM python:3.11.7-slim

WORKDIR /app
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8089
CMD ["python", "-m", "backend"]