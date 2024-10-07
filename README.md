# GCP - HTML Downloader Service by Single-File

This is a sample Python application that can be deployed on Google Cloud Platform using Cloud Run. The service downloads HTML content from a given URL using the [SingleFile CLI](https://github.com/gildas-lormeau/single-file-cli) tool and returns the text content in JSON format.

## Features

- Asynchronous HTML downloading using SingleFile.
- Flask-based web service with endpoints for downloading HTML and health checks.
- Dockerized for easy deployment on Cloud Run.

## Prerequisites

- Python 3.7+
- Docker
- Google Cloud SDK
- [SingleFile CLI](https://github.com/gildas-lormeau/single-file-cli) installed and available in your PATH.

## Setup

### Clone the Repository

```bash
git clone https://github.com/kkdai/gcp-single-file
cd gcp-single-file
```

### Install Dependencies

Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Setup

Build the Docker image:

```bash
docker build -t html-downloader-service .
```

Run the Docker container:

```bash
docker run -p 8080:8080 html-downloader-service
```

## Deployment on Google Cloud Platform

### Enable APIs

Ensure that the following APIs are enabled in your GCP project:

- Cloud Run
- Container Registry

### Deploy to Cloud Run

1. Authenticate with Google Cloud:

    ```bash
    gcloud auth login
    gcloud config set project <your-gcp-project-id>
    ```

2. Build and push the Docker image to Google Container Registry:

    ```bash
    gcloud builds submit --tag gcr.io/<your-gcp-project-id>/html-downloader-service
    ```

3. Deploy the image to Cloud Run:

    ```bash
    gcloud run deploy html-downloader-service \
        --image gcr.io/<your-gcp-project-id>/html-downloader-service \
        --platform managed \
        --region <your-region> \
        --allow-unauthenticated
    ```

## Usage

### Endpoints

- **POST /download**

  Download HTML content from a specified URL.

  **Request:**

  ```json
  {
    "url": "https://example.com"
  }
  ```

  **Response:**

  ```json
  {
    "content": "Text content of the HTML page"
  }
  ```

- **GET /**

  Health check endpoint.

## Logging

The application uses `loguru` for logging. Logs are printed to the console.

## License

This project is licensed under the MIT License.
