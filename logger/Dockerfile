FROM python:3.12-slim

WORKDIR /logger

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./logger

EXPOSE 9090

CMD ["uvicorn", "logger.main:app", "--host", "0.0.0.0", "--port", "9090"]