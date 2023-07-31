# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt requirements.txt

# Install required dependencies
RUN pip install -r requirements.txt

# Copy the entire app directory to the container
COPY . /app

# Expose the port that your Flask app listens on
EXPOSE 8080

# Set the environment variable to run the app in development mode
ENV ENV=development

# Run the Flask app when the container starts
CMD ["python", "main.py"]
