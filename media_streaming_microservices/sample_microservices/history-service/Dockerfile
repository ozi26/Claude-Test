# Use Java 17 for compilation and runtime.
FROM maven:3.9-eclipse-temurin-17 AS build
# Set the Maven working directory.
WORKDIR /build
# Copy the Maven project.
COPY sample_microservices/history-service/pom.xml ./
COPY sample_microservices/history-service/src ./src
# Build the service jar.
RUN mvn -q -DskipTests package
# Use a smaller Java runtime image.
FROM eclipse-temurin:17-jre
# Set the runtime directory.
WORKDIR /app
# Copy the compiled jar.
COPY --from=build /build/target/service-1.0.0.jar ./service.jar
# Copy the centralized Java configuration.
COPY sample_microservices/config/history.properties /app/config/history.properties
# Expose the service port.
EXPOSE 8106
# Start the service.
CMD ["java", "-jar", "service.jar"]
