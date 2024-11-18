# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app app
COPY .streamlit .streamlit

# Expose the default Streamlit port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_CONFIG_FILE=/app/.streamlit/config.toml
ENV STREAMLIT_SECRETS_FILE=/app/.streamlit/secrets.toml

# Run Streamlit
ENTRYPOINT ["streamlit", "run"]
CMD ["app/main.py"]