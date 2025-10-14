# Use a lightweight official Python image
FROM python:3.11-slim

# Set environment variables for non-buffered output and byte code skipping
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install dependencies first (better for Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# The application listens on port 5000
EXPOSE 5000

# Command to run the application using python
CMD ["python", "app.py"]
