# Use a base image of Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container
COPY requirements.txt ./
COPY app.py ./
COPY blueprints ./blueprints
COPY config.py ./
COPY utils ./utils
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the application will run
EXPOSE 5003

# Command to run the application
CMD ["python", "app.py"]
