# Use the official Python image from Docker Hub
FROM python:3.12-slim

RUN useradd -ms /bin/bash myuser
USER myuser
WORKDIR /home/myuser
ENV PATH="/home/myuser/.local/bin:${PATH}"

# Upgrade pip
RUN pip install --upgrade pip

### Models

# Install model dependencies
COPY --chown=myuser:myuser requirements_models.txt requirements_models.txt
RUN pip install --user --no-cache-dir -r requirements_models.txt

# Download models
COPY --chown=myuser:myuser app/download_models.py ./download_models/download_models.py
COPY --chown=myuser:myuser app/handlers/*_create_model.py ./download_models/
RUN python download_models/download_models.py

### App

# Install dependencies
COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy app
COPY --chown=myuser:myuser . .

EXPOSE 5000

CMD ["python", "app/run.py"]