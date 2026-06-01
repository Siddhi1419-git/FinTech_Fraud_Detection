# 1. Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# 2. Set system environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Establish the working directory inside the container
WORKDIR /app

# 4. Install system dependencies required for clean builds
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy over package dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code into the container
COPY . .

# 7. Expose the default networking port that Streamlit uses
EXPOSE 8501

# 8. Configure a container health check to monitor app stability
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 9. Run the visual dashboard automatically when the container boots up
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]