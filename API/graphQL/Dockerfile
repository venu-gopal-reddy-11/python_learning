FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install venv and create virtual environment
RUN python -m venv /opt/venv

# Activate venv and install requirements
ENV PATH="/opt/venv/bin:$PATH"

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run the app using venv Python
CMD ["python", "app.py"]
