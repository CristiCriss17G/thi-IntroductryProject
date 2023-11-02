#!/bin/bash

alembic upgrade head

# Start the server
uvicorn src.create_app:app --host ${FASTAPI10_HOST} --port ${FASTAPI10_PORT} --reload
```
