# Backend-System

A template backend project with FastAPI and Flask APIs, Nginx, Redis, and PostgreSQL in Docker.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Services](#services)
- [Endpoints](#endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Description

This project provides a template backend with two APIs built using FastAPI and Flask frameworks. It includes an Nginx server as the API gateway, Redis for caching, and PostgreSQL as the database. The Docker environment ensures easy setup and deployment, making it convenient for developers to use this template as a starting point for their backend projects.

## Installation

To use this template backend, you need to have Docker installed on your system. Follow the steps below to set up and run the project:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/S3L1M/Backend-System.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Backend-System
   ```

3. Build the Docker images and start containers:

   ```bash
   ./run.sh
   ```

The APIs will be accessible through API gateway (Ngnix) at `http://localhost:8000/inventory` (FastAPI) and `http://localhost:8000/accounts` (Flask) once the containers are up and running.

## Usage

This template backend provides two different APIs using FastAPI and Flask frameworks. You can use any of these APIs based on your preference and requirements. The API endpoints are detailed in [endpoints](#endpoints) section.

### Architecutre

<img src="https://github.com/S3L1M/Backend-System/assets/28127068/ff5c2e9a-6fa3-4d01-9578-7b52d699ea08" width=70% height=70%>

### Inventory dummy data

By defualt, inventory database will be populated with dummy data with the following code in [`inventory-service/app.py`](inventory-service/app.py) file.

```Python
# Add dummy product data
db = SessionLocal()
for i in range(1, 101):
    name = f'Product_{i}'
    price = round(random.uniform(1.99, 999.99), 2)
    description = lorem.get_sentence(count=2)
    product = Product(name=name, price=price, description=description)
    db.add(product)
db.commit()
db.close()
```

## Services

- [`inventory-service`](inventory-service)
- [`inventory-db`](docker-compose.yaml)
- [`caching-db`](docker-compose.yaml)
- [`accounts-service`](accounts-service)
- [`accounts-db`](docker-compose.yaml)
- [`API-gateway`](gateway)
- [`frontend-server`](frontend-server)

Add or remove services by modifying [`docker-compose.yaml`](docker-compose.yaml) file.

### Optional

You can add the following (redis commander) to [`docker-compose.yaml`](docker-compose.yaml) to view redis cache

```yaml
redis-commander:
   container_name: redis-commander
   hostname: redis-commander
   image: rediscommander/redis-commander:latest
   environment:
   - REDIS_HOSTS=redis:caching-db:6379
   ports:
   - "8081:8081"
```

## Endpoints

### FastAPI

- GET `/products`: Get all products.
- GET `/products/{name}`: Get a product by its name.
- GET `/products/search`: Search for products based on a keyword. \
  *Query parameters:* 
  - `keyword`: string <span style="color:#FF2400">*required</span>
- GET `/products/price-range`: Get products within a specified price range. \
  *Query parameters:* 
  - `min-price`: float <span style="color:#FF2400">*required</span> 
  - `max-price`: float <span style="color:#FF2400">*required</span>

### Flask

- GET `/users/<username>`: Get a user data.
- POST `/users`: Create a new user. \
  *Request Body:* <span style="color:#FF2400">*required</span>
  ```JSON
   {
      "username": "<string>"
      "email": "<string>"
      "password": "<string>"
   }
  ``` 
  **Note:** Authenticated is NOT implemented. Recommended: `Keycloak`

## Technologies Used

- FastAPI
- Flask
- Nginx
- Redis
- PostgreSQL
- Docker

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [Apache 2.0 License](LICENSE). Feel free to use it as a template for your backend projects.
