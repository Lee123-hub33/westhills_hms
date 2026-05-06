# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Run the app
# Command to run the API
CMD ["python", "-m", "fastapi", "run", "main.py", "--port", "8000"]