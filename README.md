# 20220092 (BOUCHET Ulysse)

This project is a python wrapper of [OpenWeather API](https://openweathermap.org/api). A docker image is available on [DockerHub](https://hub.docker.com/repository/docker/ully/weather-api/general).

## How it works

You can run the project using the following command :

```bash
docker run --env LAT="43.2970" --env LONG="5.3811" --env API_KEY=[API_KEY] ully/weather-api:0.1.1

# Example output : Marseille's current weather is clear sky. It is 21.05°C.
```

You need to set API_KEY to whatever your API key is. You can also change LAT and LONG to match whatever coordinates you want.

## Python code explanation

The python code is pretty basic and the comments should be enough explanation by themselves, but I can develop a bit more if needed.

I used the `os` package to be able to use the environment variables :

```py
# Get api key from env
api_key = os.environ.get("API_KEY")

# Get coordinates from env
lat = os.environ.get("LAT")
lon = os.environ.get("LONG")
```

I then created the URL request using the parameters :

```py
# Create URL
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
```

Finally, I used the `requests` package to send the request to the API, and extract the response data.

```py
# Send request and write response
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    city = data["name"]
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    print(f"{city}'s current weather is {weather}. It is {temp}°C.")
else:
    print("Error while requesting data from API.")
```

## Dockerfile explanation

I used the VS Code Docker extension to create my Dockerfile. I think it is cleaner as it covers more potential issues, and it is quicker to do.

However, I still wrote a simple Dockerfile myself as this is the purpose of the exercise :

```Dockerfile
# Default python image
FROM python:3.10-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Create working directory and paste contents
WORKDIR /app
COPY . /app

# Run python file
CMD ["python", "weather.py"]
```

## Commands used

Building the image :

```bash
docker build -t weather-api:0.1.1 .
```

Adding a tag to the image :

```bash
docker tag weather-api:0.1.1 ully/weather-api:0.1.1
```

Logging in :

```bash
docker login
```

Pushing the image to DockerHub :

```bash
docker push ully/weather-api:0.1.1
```

Running the image :

```bash
docker run --env LAT="43.2970" --env LONG="5.3811" --env API_KEY=[API_KEY] ully/weather-api:0.1.1
```
