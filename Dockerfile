# For more information, please refer to https://aka.ms/vscode-docker-python
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Create a workdir and copy files to it
WORKDIR /app
COPY . /app

# Expose port
EXPOSE 8081

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "weather:app", "--host", "localhost", "--port", "8081"]
