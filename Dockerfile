FROM continuumio/miniconda3

WORKDIR /workshop

RUN /opt/conda/bin/conda install jupyter

COPY environment.yml .
RUN /opt/conda/bin/conda env create --file environment.yml

COPY . .

# Run within the container and allow access without token from localhost:8888
CMD [ "conda", "run", "-n", "pandas_workshop", "jupyter", "lab", \
      "--allow-root", "--ip=0.0.0.0", "--no-browser", "--NotebookApp.token=''" ]
