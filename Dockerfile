FROM python:3.10

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    pip list

CMD ["bash", "install.sh"]
