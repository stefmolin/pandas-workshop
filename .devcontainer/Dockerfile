# https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3-miniconda/.devcontainer/base.Dockerfile
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/miniconda:${VARIANT}

# Install mamba for faster install
ENV MAMBA_EXE="/opt/mambaforge/bin/mamba"
RUN cd /tmp \
    && curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh" \
    && sudo bash Mambaforge-$(uname)-$(uname -m).sh -b -p /opt/mambaforge

# Create the conda environment
COPY environment.yml /tmp/conda-tmp/
RUN $MAMBA_EXE env create --file /tmp/conda-tmp/environment.yml --prefix /home/vscode/.conda/envs/pandas_workshop \
    && $MAMBA_EXE init

# Update PATH for Jupyter editing option
ENV PATH="/home/vscode/.conda/envs/pandas_workshop/bin:${PATH}"
ENV PROJ_LIB="/home/vscode/.conda/envs/pandas_workshop/share/proj"
