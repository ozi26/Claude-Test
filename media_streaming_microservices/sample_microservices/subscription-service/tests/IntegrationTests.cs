// Integration tests for subscription-service.
using MediaStreamX; // Import the service namespace.
using System.Net; // Import HTTP status support.
namespace Tests; // Declare the test namespace.
public class IntegrationTests { // Define HTTP integration tests.
    [Fact] public async Task HealthServerStarts() { using var cts = new CancellationTokenSource(); var app = new ServiceApp(); var port = Random.Shared.Next(12000, 15000); var task = app.RunAsync(port, "subscription-service", cts.Token); await Task.Delay(150); using var client = new HttpClient(); var response = await client.GetAsync($"http://127.0.0.1:{port}/health"); cts.Cancel(); Assert.Equal(HttpStatusCode.OK, response.StatusCode); } // Verify the live HTTP endpoint.
}
