# Your Solution
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Copy the entire project directory
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path to include the book_catalog directoryy
ENV PYTHONPATH=/app/inventory_management

# Expose port 8000
EXPOSE 9000

# Run the FastAPI app with uvicornn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]