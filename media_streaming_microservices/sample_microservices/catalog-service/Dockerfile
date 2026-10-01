# Use the Node.js 20 Alpine runtime.
FROM node:20-alpine
# Set the working directory.
WORKDIR /app
# Copy the package manifest.
COPY sample_microservices/catalog-service/package.json ./
# Install dependencies.
RUN npm install
# Copy source and tests.
COPY sample_microservices/catalog-service/src ./src
COPY sample_microservices/catalog-service/tests ./tests
# Copy centralized configuration.
COPY sample_microservices/config/catalog.config.js /app/config/catalog.config.js
# Expose the service port.
EXPOSE 8101
# Start the service.
CMD ["node", "src/app.js"]
