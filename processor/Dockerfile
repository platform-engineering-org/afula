FROM registry.access.redhat.com/ubi10/python-312-minimal:10.1-1770208168

WORKDIR /app

COPY db/ ./db/
COPY processor/ ./processor/

RUN pip install -r processor/requirements.txt

CMD ["python", "-m", "processor.main"]
