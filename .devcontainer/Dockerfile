ARG VARIANT=2
FROM mcr.microsoft.com/devcontainers/universal:${VARIANT}

# Create the conda environment
COPY environment.yml /tmp/conda-tmp/
RUN conda env create --file /tmp/conda-tmp/environment.yml

# Update PATH for Jupyter editing option
ENV PATH="/opt/conda/envs/pandas_workshop/bin:${PATH}"
