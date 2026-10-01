// Catalog service: stores and serves the media catalogue.
const http = require('http'); // Load Node's built-in HTTP server.
const config = require('/app/config/catalog.config'); // Load centralized JavaScript configuration.

const movies = [ // Create the in-memory catalogue used by this prototype.
  { id: 'm1', title: 'Ocean Signal', genre: 'Drama', year: 2026 }, // Define the first media item.
  { id: 'm2', title: 'Night Circuit', genre: 'Thriller', year: 2025 }, // Define the second media item.
  { id: 'm3', title: 'Green Horizon', genre: 'Adventure', year: 2024 }, // Define the third media item.
]; 
// Finish the catalogue list.

function sendJson(res, status, body) { // Send a JSON HTTP response.
  res.writeHead(status, { 'Content-Type': 'application/json' }); // Set the response status and content type.
  res.end(JSON.stringify(body)); // Serialize the body and finish the response.
} 
// End sendJson.

function getMovie(id) { // Find one media item by its identifier.
  return movies.find((movie) => movie.id === id); // Return the matching item or undefined.
} 
// End getMovie.

function handleRequest(req, res) { // Handle one incoming HTTP request.
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`); // Parse the request URL.
  if (url.pathname === '/health' && req.method === 'GET') return sendJson(res, 200, { status: 'ok', service: config.serviceName }); // Respond to health checks.
  if (url.pathname === '/movies' && req.method === 'GET') return sendJson(res, 200, movies); // Return the complete catalogue.
  const match = url.pathname.match(/^\/movies\/([^/]+)$/); // Check for a single-media route.
  if (match && req.method === 'GET') { const movie = getMovie(match[1]); return movie ? sendJson(res, 200, movie) : sendJson(res, 404, { error: 'Movie not found' }); } // Return one media item or an error.
  return sendJson(res, 404, { error: 'Route not found' }); // Reject unknown routes.
} // End handleRequest.

function createServer() { // Create and return the configured HTTP server.
  return http.createServer(handleRequest); // Build a server around the request handler.
} // End createServer.

if (require.main === module) { // Start the network server only when executed directly.
  createServer().listen(config.port, () => console.log(`${config.serviceName} listening on ${config.port}`)); // Listen on the configured port.
} // End direct execution block.

module.exports = { createServer, movies, getMovie, handleRequest }; // Export testable service functions.
