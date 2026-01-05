# Use an official Python runtime as a parent image
# "slim" variants are smaller and faster to build
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements first to leverage Docker cache
# (This prevents re-installing pip packages every time you change a line of code)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# Note: We use python serve.py because your serve.py includes uvicorn.run()
CMD ["python", "serve.py"]