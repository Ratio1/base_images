FROM pytorch/pytorch

WORKDIR /aixp_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV AIXP_ENV="base_th_llm_fastapi"
ENV AIXP_ENV_VER = "0.1.0"