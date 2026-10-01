// Central configuration for the catalog JavaScript service.
module.exports = { port: Number(process.env.CATALOG_PORT || 8101), serviceName: 'catalog-service' }; // Export the port and service name.
