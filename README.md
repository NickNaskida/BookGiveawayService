# Book Giveaway Service

### Author Note

### Project Note
 - Register endpoint ignores `is_active`, `is_superuser`, `is_verified` fields. That's a FastAPI-Users specification
 - After registration user is not verified. You can obtain verification token through app logs (it will be logged out and printed to console) or just connect to db on `localhost:5432` `password & username: postgres` and edit `is_verified` field to `true`

### Project Structure
```
.
```

### Setup

### License
Project is distributed under MIT License. See `LICENSE.txt` for more information.

