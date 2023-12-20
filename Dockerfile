FROM continuumio/miniconda3:latest

WORKDIR /app

COPY ./* /app

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "listify_api", "/bin/bash", "-c"]

RUN echo "Make sure fastapi is installed:"
RUN python -c "import fastapi"

EXPOSE 8000

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "listify_api", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
