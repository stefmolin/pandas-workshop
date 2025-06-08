# https://github.com/devcontainers/images/tree/main/src/miniconda
ARG VARIANT=3
FROM mcr.microsoft.com/devcontainers/miniconda:${VARIANT}

# Create the conda environment
COPY environment.yml /tmp/conda-tmp/
RUN conda env create --file /tmp/conda-tmp/environment.yml --prefix /home/vscode/.conda/envs/pandas_workshop \
    && conda init

# Update PATH for Jupyter editing option
ENV PATH="/home/vscode/.conda/envs/pandas_workshop/bin:${PATH}"
ENV PROJ_LIB="/home/vscode/.conda/envs/pandas_workshop/share/proj"
