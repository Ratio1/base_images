ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION}

WORKDIR /aixp_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV AIXP_ENV="base_fastapi_${PYTHON_VERSION}"
ENV AIXP_ENV_VER = "0.1.0"
