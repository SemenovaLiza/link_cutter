FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000

COPY . /app

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]