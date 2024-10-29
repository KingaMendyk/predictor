# Start with lightweight Python image
FROM python:3.9-slim

# Set environment variables to avoid .pyc files and set the Python buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first, for better caching
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server using Uvicorn
CMD ["uvicorn", "predictor:app", "--host", "0.0.0.0", "--port", "8000"]
