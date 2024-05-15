FROM pytorch/pytorch

WORKDIR /ai_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV AID_APP_SHOW_PACKS=Yes \
    AID_APP_FORCE_CPU=No \
    AID_APP_DOCKER=Yes \
    AID_APP_ID=BaseAidApp \
    AID_APP_ENV=v2

ENV AID_ENV_NAME="base_th_llm_fastapi"
ENV AID_ENV_VER = "0.2.1"

# Generate desired locale
RUN locale-gen en_US.UTF-8

# Set environment variables for locale
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     