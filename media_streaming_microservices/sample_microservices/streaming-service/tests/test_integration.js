// Integration tests for the streaming HTTP API.
const http = require('http'); // Load the HTTP client.
const { createServer } = require('../src/app'); // Import the real server.

function request(port, body) { // Send a POST request to the service.
  return new Promise((resolve, reject) => { const payload = JSON.stringify(body); const req = http.request({ hostname: '127.0.0.1', port, path: '/stream/start', method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) } }, (res) => { let data = ''; res.on('data', (chunk) => data += chunk); res.on('end', () => resolve({ status: res.statusCode, body: JSON.parse(data) })); }); req.on('error', reject); req.write(payload); req.end(); }); } // Finish the helper.

test('creates a playback session through HTTP', async () => { // Test the real endpoint.
  const server = createServer().listen(0); // Start the actual server.
  const result = await request(server.address().port, { userId: 'u1', mediaId: 'm1' }); // Call the endpoint.
  server.close(); // Stop the test server.
  expect(result.status).toBe(201); // Check creation status.
  expect(result.body.mediaId).toBe('m1'); // Check returned media ID.
}); // End integration test.
