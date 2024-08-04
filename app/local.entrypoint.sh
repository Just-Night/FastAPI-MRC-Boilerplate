#!/bin/sh

uvicorn "_main_:app" --host 0.0.0.0 --port 8000 --reload --access-log 
