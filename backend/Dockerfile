
# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install dependencies from the requirements file
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the API port
EXPOSE 7860

# Start the Flask API using Gunicorn
# -w 4 : Use 4 worker processes
# -b 0.0.0.0:7860 : Bind to port 7860 on all interfaces
# app:superkart_api :
#     app.py contains the Flask application instance
#     named 'superkart_api'

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
