# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app's code into the container
COPY . .

# Expose the port FastAPI is running on (port 8000)
EXPOSE 8000

# Command to run FastAPI using Uvicorn (ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
