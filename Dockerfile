FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir discord.py

COPY bot.py .

ENV PYTHONUNBUFFERED=1

CMD python bot.py
