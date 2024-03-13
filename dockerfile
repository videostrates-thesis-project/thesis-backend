# Use an official python image as a base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY src/ ./

# Expose the port that the flask app runs on
EXPOSE 5000

# Run the flask app using gunicorn as the HTTP server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
