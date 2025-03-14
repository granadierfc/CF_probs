# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-b", ":8080", "app:app"]
