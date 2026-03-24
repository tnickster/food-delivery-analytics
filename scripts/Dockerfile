FROM python:3.12-slim

#Set working dir
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_data.py .

#defualt command when container starts
CMD ["python", "extract_data.py"]

