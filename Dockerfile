FROM python:3.8

WORKDIR /FastAPI_Boilerplate

COPY requirements.txt /FastAPI_Boilerplate/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FastAPI_Boilerplate/requirements.txt

COPY . /FastAPI_Boilerplate

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
