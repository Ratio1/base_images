ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION}

WORKDIR /ai_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV AI_ENV_NAME="base_fastapi_${PYTHON_VERSION}"
ENV AI_ENV_VER = "0.1.1"
