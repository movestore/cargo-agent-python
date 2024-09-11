FROM condaforge/miniforge3:latest
LABEL org.opencontainers.image.authors="us@couchbits.com"
LABEL org.opencontainers.image.vendor="couchbits GmbH"

ENV PROJECT_DIR=/opt/cargo-agent-python
ENV ENV_PREFIX=$PROJECT_DIR/conda
RUN mkdir $PROJECT_DIR

# Security Aspects
ENV UID=moveapps
ENV GID=moveapps
RUN addgroup --system $GID && adduser --system $UID --ingroup $GID
RUN chown $UID:$GID $PROJECT_DIR

USER $UID:$GID
WORKDIR $PROJECT_DIR

# setup runtime environment
COPY --chown=$UID:$GID environment.yml $PROJECT_DIR
RUN conda env create --prefix $ENV_PREFIX --file $PROJECT_DIR/environment.yml && \
    conda clean --all --yes

# the app
COPY --chown=$UID:$GID main.py .
COPY --chown=$UID:$GID src/ ./src/

CMD [ "conda", "run", "--no-capture-output", "--prefix", "${ENV_PREFIX}", "python3", "main.py"]