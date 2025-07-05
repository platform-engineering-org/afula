FROM registry.access.redhat.com/ubi10/python-312-minimal:10.0-1747316123

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "processor.py"]
