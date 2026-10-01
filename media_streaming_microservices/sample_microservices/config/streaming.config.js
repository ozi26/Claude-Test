// Central configuration for the streaming JavaScript service.
module.exports = { port: Number(process.env.STREAMING_PORT || 8102), serviceName: 'streaming-service' }; // Export the port and service name.
