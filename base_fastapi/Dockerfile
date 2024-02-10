ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION}
WORKDIR /aixp_fastapi_app
RUN pip install fastapi uvicorn redis numpy pydantic psycopg2-binary python-multipart
ENV AIXP_ENV="base_fastapi_${PYTHON_VERSION}"
