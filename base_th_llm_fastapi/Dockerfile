FROM pytorch/pytorch

WORKDIR /ai_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV AID_ENV_NAME="base_th_llm_fastapi"
ENV AID_ENV_VER = "0.1.1"