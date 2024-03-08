FROM python:3.9

WORKDIR /app

COPY requirements.txt .

# Copy the templates folder into the container
COPY templates/ templates/

# Copy the templates folder into the container
COPY static/ static/

COPY methods/ methods/

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
