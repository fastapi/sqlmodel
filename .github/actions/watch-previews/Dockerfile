FROM python:3.8

RUN pip install httpx PyGithub "pydantic==1.5.1"

COPY ./app /app

CMD ["python", "/app/main.py"]
