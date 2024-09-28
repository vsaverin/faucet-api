# Faucet API - Django REST Framework

This is a simple Django REST Framework (DRF) application that implements a cryptocurrency faucet. It allows users to request a small amount (```0.0001```) of ETH to be sent to a specified wallet address. The application includes rate-limiting to prevent abuse and provides statistics on transactions (successful and failed) made through the faucet.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [License](#license)

## Features

- Request ETH to be sent to a wallet address
- Rate-limited to one request per minute per IP address
- Fetch statistics on successful and failed transactions in the past 24 hours
- Error handling for failed transactions

## Installation

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.11
- poetry
- Docker and docker-compose (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/vsaverin/faucet-api.git
cd faucet-api
```

### Step 2: Create and Activate Virtual Environment

```bash
poetry shell
```

### Step 3: Install Dependencies

```bash
poetry install
```

### Step 4: Set Up Environment Variables

Create a `.env` file in `./deploy` and define the following environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
NODE_URL="https node url"
SOURCE_WALLET="wallet to send eth from"
PRIVATE_KEY="and its private key"

```

### Step 5: Apply migrations

```bash
pythone manage.py migrate
```

### Step 6: Create a Superuser

```bash
python3 manage.py createsuperuser
```

### Step 7: Run the Development Server

```bash
python3 manage.py runserver
```

## Or using Docker

### Step 1: Build and run the containers

```bash
docker-compose -f ./deploy/docker-compose.yml up --build
```

### Step 2: Apply migrations

```bash
docker-compose -f ./deploy/docker-compose.yml run web python manage.py migrate
```

### Step 2: Create superuser

```bash
docker-compose -f ./deploy/docker-compose.yml run web python manage.py createsuperuser
```
---

Now application is available at `http://localhost:8000/`
Swagger API Documentation is available at `http://localhost:8000/api/schema/swagger-ui/`

## API Endpoints

### 1. **Fund Wallet (POST /faucet)**

#### Description:
Send 0.0001 ETH to the specified wallet address. Rate-limited to one request per minute per IP address.

- **URL:** `/faucet`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "wallet_address": "0xYourWalletAddress"
  }
  ```
- **Response Example (200 OK):**
  ```json
  {
    "tx_id": "0xTransactionHash"
  }
  ```
- **Response Example (429 Rate Limited):**
  ```json
  {
    "error": "Rate limit exceeded. Please wait 1 minute."
  }
  ```

### 2. **Get Faucet Stats (GET /faucet/stats)**

#### Description:
Get the statistics for the faucet over the past 24 hours. Returns the count of successful and failed transactions.

- **URL:** `/faucet/stats`
- **Method:** GET
- **Response Example (200 OK):**
  ```json
  {
    "successful_transactions": 10,
    "failed_transactions": 2
  }
  ```

## Running Tests

### Step 1: Run all tests

```bash
python3 manage.py test
```
