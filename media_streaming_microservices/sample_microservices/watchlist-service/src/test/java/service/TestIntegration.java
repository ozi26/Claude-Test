package service; // Declare the test package.

import org.junit.jupiter.api.Test; // Import JUnit tests.
import java.net.*; // Import HTTP networking.
import java.net.http.*; // Import the Java HTTP client.
import static org.junit.jupiter.api.Assertions.*; // Import assertions.

class TestIntegration { // Define HTTP integration tests.
    @Test void healthEndpointWorks() throws Exception { WatchlistService service=WatchlistService.create(); var server=service.server(0); server.start(); var client=HttpClient.newHttpClient(); var request=HttpRequest.newBuilder(URI.create("http://127.0.0.1:"+server.getAddress().getPort()+"/health")).GET().build(); var response=client.send(request,HttpResponse.BodyHandlers.ofString()); server.stop(0); assertEquals(200,response.statusCode()); assertTrue(response.body().contains("ok")); } // Verify the live HTTP endpoint.
}
