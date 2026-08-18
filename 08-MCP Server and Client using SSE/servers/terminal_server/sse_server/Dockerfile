# Use the official Python 3.11-slim image as the base image.
FROM python:3.11-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy all files from the current directory into /app in the container.
COPY . /app

# Install required Python packages from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8081 so that the container can accept incoming connections.
EXPOSE 8081

# Define the command to run your SSE server.
CMD ["python", "terminal_server_sse.py"]