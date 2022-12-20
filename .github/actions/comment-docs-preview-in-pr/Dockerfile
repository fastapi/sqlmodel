FROM python:3.8

RUN pip install httpx "pydantic==1.8.2" pygithub

COPY ./app /app

CMD ["python", "/app/main.py"]
