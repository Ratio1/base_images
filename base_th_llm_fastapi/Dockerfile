FROM pytorch/pytorch

WORKDIR /ai_fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    locales \
    # iputils-ping \
    # tzdata \
    # nano \
    # vim \
    # curl \
    # git \
    # htop \
    # Clean up apt cache to reduce image size
    && apt-get clean && rm -rf /var/lib/apt/lists/*   

ENV AID_APP_SHOW_PACKS=Yes \
    AID_APP_FORCE_CPU=No \
    AID_APP_DOCKER=Yes \
    AID_APP_ID=BaseAidApp \
    AID_APP_ENV=v2

ENV AID_ENV_NAME="base_th_llm_fastapi"
ENV AID_ENV_VER = "0.2.2"

# Generate desired locale
RUN locale-gen en_US.UTF-8

# Set environment variables for locale
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     