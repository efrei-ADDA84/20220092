# Use base python image
FROM python:3.10-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Create a workdir and copy files to it
WORKDIR /app
COPY . /app

# Start API
CMD ["uvicorn", "weather:app", "--host", "0.0.0.0", "--port", "8081"]
