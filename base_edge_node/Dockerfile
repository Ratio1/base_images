FROM pytorch/pytorch

WORKDIR /ai_edge_node

COPY requirements.txt .

RUN conda install -c conda-forge "transformers>=4.38.0" "ffmpeg>=5" "pyarrow>=15" \
    && conda install seaborn pandas shapely scikit-learn scikit-image dropbox pymssql h5py unidecode jupyter\
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && conda clean -afy

RUN pip install --no-cache-dir -r requirements.txt

ENV AI_ENV="base_edge_node"
ENV AI_ENV_VER = "0.1.1"