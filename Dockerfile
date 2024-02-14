FROM python:3.10

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt && pip install openai==0.28

CMD ["python3", "client.py"]
