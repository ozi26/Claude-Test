// Integration tests for the catalog HTTP API.
const http = require('http'); // Load the HTTP client.
const { createServer } = require('../src/app'); // Import the real service server.

function request(port, path) { // Send a GET request to the running service.
  return new Promise((resolve, reject) => { const req = http.get({ hostname: '127.0.0.1', port, path }, (res) => { let data = ''; res.on('data', (chunk) => data += chunk); res.on('end', () => resolve({ status: res.statusCode, body: JSON.parse(data) })); }); req.on('error', reject); }); } // Finish the HTTP helper.

test('serves health endpoint', async () => { // Test the real HTTP endpoint.
  const server = createServer().listen(0); // Start the actual server on an ephemeral port.
  const result = await request(server.address().port, '/health'); // Call the health route.
  server.close(); // Stop the test server.
  expect(result.status).toBe(200); // Check HTTP status.
  expect(result.body.status).toBe('ok'); // Check service response.
}); // End integration test.
