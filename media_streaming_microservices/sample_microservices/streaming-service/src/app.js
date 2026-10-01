// Streaming service: creates playback sessions for media items.
const http = require('http'); // Load Node's built-in HTTP server.
const config = require('/app/config/streaming.config'); // Load centralized configuration.

function createPlaybackSession(userId, mediaId) { // Build a playback session for a user and media item.
  if (!userId || !mediaId) throw new Error('userId and mediaId are required'); // Validate required values.
  return { sessionId: `${userId}-${mediaId}-${Date.now()}`, userId, mediaId, playbackUrl: `http://localhost:8102/media/${mediaId}/manifest.m3u8` }; // Return session metadata.
} // End createPlaybackSession.

function sendJson(res, status, body) { // Send a JSON response.
  res.writeHead(status, { 'Content-Type': 'application/json' }); // Set response headers.
  res.end(JSON.stringify(body)); // Serialize and finish the response.
} // End sendJson.

function readBody(req) { // Read a JSON request body.
  return new Promise((resolve, reject) => { let data = ''; req.on('data', (chunk) => data += chunk); req.on('end', () => { try { resolve(JSON.parse(data || '{}')); } catch (error) { reject(error); } }); req.on('error', reject); }); // Collect and parse the body.
} // End readBody.

function createServer() { // Create the streaming HTTP server.
  return http.createServer(async (req, res) => { // Create an asynchronous request handler.
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`); // Parse the request URL.
    if (url.pathname === '/health' && req.method === 'GET') return sendJson(res, 200, { status: 'ok', service: config.serviceName }); // Serve health checks.
    if (url.pathname === '/stream/start' && req.method === 'POST') { try { const body = await readBody(req); return sendJson(res, 201, createPlaybackSession(body.userId, body.mediaId)); } catch (error) { return sendJson(res, 400, { error: error.message }); } } // Create playback sessions.
    return sendJson(res, 404, { error: 'Route not found' }); // Reject unknown routes.
  }); // Finish server creation.
} // End createServer.

if (require.main === module) createServer().listen(config.port, () => console.log(`${config.serviceName} listening on ${config.port}`)); // Start the service when executed directly.
module.exports = { createServer, createPlaybackSession }; // Export functions for tests.
