# Use Python 3.12.
FROM python:3.12-slim
# Set the working directory.
WORKDIR /app
# Copy source and tests.
COPY sample_microservices/recommendation-service/src ./src
COPY sample_microservices/recommendation-service/tests ./tests
# Copy centralized configuration.
COPY sample_microservices/config/recommendation_config.py /app/config/recommendation_config.py
# Expose the service port.
EXPOSE 8104
# Start the service.
CMD ["python", "src/app.py"]
