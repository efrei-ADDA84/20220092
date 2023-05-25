# 20220092 (BOUCHET Ulysse)

_Note : This is the report for TP3. You can read the [TP2 report here](https://github.com/efrei-ADDA84/20220092/blob/090a61af9bf97a14d031e6bf9d650bf64af62ffa/README.md) and the [TP1 report here](https://github.com/efrei-ADDA84/20220092/blob/5bcaf1b8b63cbcbaf9e2afbe32282e715395b4f1/README.md)._

This project is an API that wraps [OpenWeather API](https://openweathermap.org/api). A docker image is available on [DockerHub](https://hub.docker.com/repository/docker/ully/weather-api/general).

## How it works

It's very simple ! You just have to use a `curl` command, using the `lon` and `lat` parameters :

```bash
curl "http://devops-20220092.francecentral.azurecontainer.io:8081/?lat={lat}&lon={lon}"
```

_/!\ Don't forget to specify the 8081 port!_

Here's an example response you can get :

```json
{
  "city": "Marseille",
  "weather": "overcast clouds",
  "temperature": 22.16
}
```

You can also request the API directly in your browser, using the same URL as above.

## Azure Workflow explanation

I have created a workflow that automatically builds and pushes an image to the Azure Container Registry every time something is pushed on GitHub. In order to keep my Docker login data private, I used GitHub Action's secrets.

Using a workflow instead of the Azure CLI makes everything automated, making it easier for the developer to just push their code without having any extra steps.

```yml
name: Azure Publish

on:
  push:
    branches:
      - main

jobs:
  build-and-publish:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: "Login via Azure CLI"
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Login to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220092:latest .
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220092:latest

      - name: "Deploy to Azure Container Instances"
        uses: "azure/aci-deploy@v1"
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: devops-20220092
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220092:latest
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: 20220092
          location: "france central"
          secure-environment-variables: API_KEY=${{ secrets.OPENWEATHER_API_KEY }}
          ports: 8081
```

Please not that I added the API Key as a secret environment variable for security issues. I also specified the port.
