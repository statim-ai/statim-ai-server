FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-poetry

RUN useradd -ms /bin/bash statim
USER statim
WORKDIR /home/statim
ENV PATH="/home/statim/.local/bin:${PATH}"

# Upgrade pip
RUN pip install --upgrade pip

# Install app dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --only main

# Install model dependencies
RUN poetry install --no-root --only models

# Download models
COPY --chown=statim:statim app/download_models.py ./download_models/download_models.py
COPY --chown=statim:statim app/handlers/ ./download_models/
RUN poetry run python download_models/download_models.py

# Copy app
COPY --chown=statim:statim . .

EXPOSE 5000

CMD ["poetry", "run", "python", "app/run.py"]