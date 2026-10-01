# Use the .NET 8 SDK for building.
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
# Set the build directory.
WORKDIR /src
# Copy the project file.
COPY sample_microservices/subscription-service/subscription-service.csproj ./
# Restore project dependencies.
RUN dotnet restore
# Copy the service source.
COPY sample_microservices/subscription-service/Service.cs ./
# Build the service.
RUN dotnet publish -c Release -o /app/publish
# Use the smaller .NET 8 runtime image.
FROM mcr.microsoft.com/dotnet/runtime:8.0
# Set the runtime directory.
WORKDIR /app
# Copy published files.
COPY --from=build /app/publish ./
# Copy the centralized C# configuration.
COPY sample_microservices/config/subscription.json /app/config/subscription.json
# Expose the service port.
EXPOSE 8107
# Start the service.
ENTRYPOINT ["dotnet", "subscription-service.dll"]
