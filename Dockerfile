from python:3.11

run mkdir /fastapi_app

workdir /fastapi_app

copy requirements.txt .

run pip install --upgrade pip
run pip install -r requirements.txt

copy . .

cmd gunicorn currency:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000