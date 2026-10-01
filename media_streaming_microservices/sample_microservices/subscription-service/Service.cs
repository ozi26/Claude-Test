// Define the namespace for this service.
using System.Net;
using System.Text;
using System.Text.Json;

namespace MediaStreamX;

public class ServiceApp
{
    private readonly Dictionary<string, string> _data = new(); // Store prototype state in memory.
    public string Subscribe(string userId, string plan) { _data[userId] = plan; return plan; } // Save a subscription.
    public string? GetSubscription(string userId) { return _data.TryGetValue(userId, out var plan) ? plan : null; } // Read a subscription.
    public async Task RunAsync(int port, string serviceName, CancellationToken token) // Start the HTTP server.
    {
        using var listener = new HttpListener(); // Create the standard .NET HTTP listener.
        listener.Prefixes.Add($"http://127.0.0.1:{port}/"); // Bind to localhost and the requested port.
        listener.Start(); // Start listening.
        while (!token.IsCancellationRequested) // Continue while the service is active.
        {
            var context = await listener.GetContextAsync().WaitAsync(token); // Wait for the next HTTP request while honoring cancellation.
            _ = Task.Run(() => HandleAsync(context, serviceName)); // Handle the request without blocking other requests.
        }
    }
    private async Task HandleAsync(HttpListenerContext context, string serviceName) // Process one HTTP request.
    {
        var path = context.Request.Url!.AbsolutePath; // Read the request path.
        if (path == "/health") { await JsonAsync(context, 200, new { status = "ok", service = serviceName }); return; } // Serve health checks.
        if (path == "/subscribe" && context.Request.HttpMethod == "POST") { using var reader = new StreamReader(context.Request.InputStream); var body = JsonSerializer.Deserialize<Dictionary<string,string>>(await reader.ReadToEndAsync()) ?? new(); var plan = Subscribe(body.GetValueOrDefault("userId", ""), body.GetValueOrDefault("plan", "basic")); await JsonAsync(context, 201, new { status = "subscribed", plan }); return; } // Create subscriptions.
        if (path.StartsWith("/subscription/") && context.Request.HttpMethod == "GET") { var userId = path.Split('/').Last(); var plan = GetSubscription(userId); await JsonAsync(context, 200, new { userId, plan }); return; } // Read subscriptions.
        await JsonAsync(context, 404, new { error = "Route not found" }); // Reject unknown routes.
    }
    private static async Task JsonAsync(HttpListenerContext context, int status, object body) // Send a JSON response.
    {
        var bytes = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(body)); // Serialize the body.
        context.Response.StatusCode = status; // Set the HTTP status.
        context.Response.ContentType = "application/json"; // Set the response content type.
        context.Response.ContentLength64 = bytes.Length; // Set the response length.
        await context.Response.OutputStream.WriteAsync(bytes); // Write the response body.
        context.Response.Close(); // Close the response stream.
    }
}

public static class Program
{
    public static async Task Main() // Start the service process.
    {
        var app = new ServiceApp(); // Create the service instance.
        var port = int.Parse(Environment.GetEnvironmentVariable("PORT") ?? "8107"); // Read the configured port.
        using var stop = new CancellationTokenSource(); // Create a cancellation source.
        Console.CancelKeyPress += (_, e) => { e.Cancel = true; stop.Cancel(); }; // Stop gracefully on Ctrl+C.
        await app.RunAsync(port, "subscription-service", stop.Token); // Run the HTTP service.
    }
}
