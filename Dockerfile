from python:3.11

run mkdir /fastapi_app

workdir /fastapi_app

copy requirements.txt .

run pip install --upgrade pip
run pip install -r requirements.txt

copy . .

RUN chmod a+x docker/*.sh


# workdir src
#
# cmd gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000