FROM python:3.9-slim

# Set the working directory
WORKDIR /opt/app

# Copy only requirements first (to leverage Docker layer caching)
COPY requirements.txt /opt/app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /opt/app/

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ "tail", "-f", "/dev/null" ]
