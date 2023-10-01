# Book Giveaway Service

### Project Note
 - Register endpoint ignores `is_active`, `is_superuser`, `is_verified` fields. That's a FastAPI-Users specification
 - **Testing is not fully complete**. I've wrote tests for only a few endpoints for demonstration purposes. (Sorry didn't manage to finish it in time)
 - **Test users**:
    
    ```
    # Superuser, email verified
    Email: admin@gmail.com
    Password: admin
    
    # Plain users, email verified
    Email: test1@gmail.com
    Password: test1
    
    Email: test2@gmail.com
    Password: test2
    ```

### Project Stack
 - Python 3.10
 - FastAPI
 - PostgreSQL
 - Redis
 - Docker
 - Docker Compose
 - Pytest

### Project Structure
```
.
```

### Setup
1. Clone the repository
    ```
    git clone https://github.com/NickNaskida/BookGiveawayService.git
    ```

2. Navigate to the project root
    ```
    cd BookGiveawayService
    ```

3. Copy env file in `envs` directory
    ```
    cp example.env .env
    ```

4. Run docker compose
    ```
    docker-compose up -d --build
    ```
   
5. Enjoy!
    ```
    http://localhost:8000
    ```

### License
Project is distributed under MIT License. See `LICENSE.txt` for more information.

