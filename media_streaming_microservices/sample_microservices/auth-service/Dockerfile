# Use a stable Python runtime image.
FROM python:3.12-slim
# Set the service working directory.
WORKDIR /app
# Copy the service source code.
COPY sample_microservices/auth-service/src ./src
# Copy the service tests.
COPY sample_microservices/auth-service/tests ./tests
# Copy the centralized Python configuration.
COPY sample_microservices/config/auth_config.py /app/config/auth_config.py
# Expose the service port.
EXPOSE 8103
# Start the service.
CMD ["python", "src/app.py"]
