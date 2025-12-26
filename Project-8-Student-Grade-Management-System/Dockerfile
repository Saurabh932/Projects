FROM python:3.11-slim

# Setting working directory
WORKDIR /app

# Installing system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose Fastapi port
EXPOSE 8000

# Start server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]