FROM condaforge/miniforge3:latest
LABEL org.opencontainers.image.authors="us@couchbits.com"
LABEL org.opencontainers.image.vendor="couchbits GmbH"

ENV PROJECT_DIR /opt/cargo-agent-python
ENV ENV_PREFIX=${PROJECT_DIR}/conda

# the app
WORKDIR $PROJECT_DIR
COPY main.py environment.yml ./
COPY src/ ./src/
COPY test/ ./test/
RUN conda env create --prefix ${ENV_PREFIX}  --file environment.yml && \
    conda clean --all --yes

RUN conda run --prefix ${ENV_PREFIX} python3 -m unittest