# afula

Renovate Management

## Local Development & Execution

### Prerequisites
- Docker installed

### Build & Run Locally
1.  Build the container image:
    ```bash
    docker build -t ghcr.io/platform-engineering-org/afula:latest .
    ```
2.  Run the application:
    ```bash
    docker run -p 5000:5000 ghcr.io/platform-engineering-org/afula:latest
    ```
3.  Access the application at `http://127.0.0.1:5000`.
