# 20220092 (BOUCHET Ulysse)

*Note : This is the report for TP2. Please go [back to the previous version](https://github.com/efrei-ADDA84/20220092/blob/5bcaf1b8b63cbcbaf9e2afbe32282e715395b4f1/README.md) if you want to read the TP1 report.*

This project is an API that wraps [OpenWeather API](https://openweathermap.org/api). A docker image is available on [DockerHub](https://hub.docker.com/repository/docker/ully/weather-api/general).

## How it works

You can start the API using the following command :

```bash
docker run -p 8081:8081 --env API_KEY=[API_KEY] ully/weather-api:latest
```

You need to set `API_KEY` to whatever your API key is.

Then, you can make some requests to the API (you need to set the `lat` and `lon` parameters) :

```bash
curl "http://localhost:8081/?lat={lat}&lon={lon}"
```

Here's an example response you can get :

```json
{
    "city": "Marseille",
    "weather": "overcast clouds",
    "temperature": 22.16
}
```

You can also request the API directly in your browser, using the same URL as above.

## Python code explanation

First, I retrieve the API key using the `os` package :

```py
api_key = os.environ.get("API_KEY")
```

I decided to use `FastAPI` to develop this API, because I already use it at work so I know how it works.

I first instantiate the API, and create a route :

```py
# Create API
app = FastAPI()


# Create route
@app.get("/")
def weather(lat: float, lon: float, api_key: str = os.environ.get("API_KEY")):
```

Inside the weather route, I request the OpenWeather API, wrap and return the results unless an error occurs :

```py
# Create URL
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

# Request data
response = requests.get(url)

# If valid response
if response.status_code == 200:
    # Wrap it
    data = response.json()
    city = data["name"]
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]

    # Return it
    return {"city": city, "weather": weather, "temperature": temp}
else:
    # Return an error
    return {"error": "Error while requesting data from API."}
```

## Dockerfile explanation

I wrote a simple Dockerfile that uses a python base image : 

```Dockerfile
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
```

*Note : This time, the final command ran is an uvicorn command, that starts the server.*

## Workflow explanation

I have created a workflow that automatically builds and pushes an image to the DockerHub repository every time something is pushed on GitHub. In order to keep my Docker login data private, I used GitHub Action's secrets.

```yml
name: Docker Publish

on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_USERNAME }} # using secrets to hide data
        password: ${{ secrets.DOCKER_PASSWORD }} # using secrets to hide data
    - name: Build the Docker image
      run: docker build . -t ully/weather-api:latest
    - name: Push the Docker image
      run: docker push ully/weather-api:latest

```

