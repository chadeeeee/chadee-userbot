FROM python:3.10

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

CMD ["python3", "client.py"]
