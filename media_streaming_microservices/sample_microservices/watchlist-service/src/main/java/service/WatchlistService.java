package service; // Declare the service package.

import com.sun.net.httpserver.HttpExchange; // Import the HTTP exchange type.
import com.sun.net.httpserver.HttpServer; // Import the standard HTTP server.
import java.io.*; // Import Java IO helpers.
import java.net.InetSocketAddress; // Import network address support.
import java.nio.charset.StandardCharsets; // Import UTF-8 support.
import java.util.*; // Import collection helpers.

public class WatchlistService { // Define the WatchlistService service class.
    private static final Map<String, List<String>> DATA = new HashMap<>(); // Keep prototype data in memory.
    public static WatchlistService create() { return new WatchlistService(); } // Create the service object for tests.
    public void add(String userId, String mediaId) { DATA.computeIfAbsent(userId, key -> new ArrayList<>()).add(mediaId); } // Add one media item.
    public List<String> list(String userId) { return DATA.getOrDefault(userId, List.of()); } // Return saved items.
    public HttpServer server(int port) throws IOException { // Create the HTTP server.
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", port), 0); // Bind the server.
        server.createContext("/health", this::health); // Register the health route.
        server.createContext("/watchlist", this::api); // Register the service route.
        return server; // Return the configured server.
    }
    private void health(HttpExchange exchange) throws IOException { write(exchange, 200, "{\"status\":\"ok\",\"service\":\"watchlist-service\"}"); } // Respond to health checks.
    private void api(HttpExchange exchange) throws IOException { // Handle service requests.
        if (exchange.getRequestMethod().equals("GET")) { String user = query(exchange, "userId", "u1"); write(exchange, 200, "{\"userId\":\"" + user + "\",\"mediaIds\":" + list(user).toString().replace("=", "") + "}"); return; } // Handle GET listing.
        if (exchange.getRequestMethod().equals("POST")) { String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8); String user = value(body, "userId"); String media = value(body, "mediaId"); add(user, media); write(exchange, 201, "{\"status\":\"added\"}"); return; } // Handle POST creation.
        write(exchange, 405, "{\"error\":\"Method not allowed\"}"); // Reject unsupported methods.
    }
    private String query(HttpExchange e, String key, String fallback) { String q=e.getRequestURI().getQuery(); if(q==null)return fallback; for(String item:q.split("&")){String[] p=item.split("="); if(p.length==2&&p[0].equals(key))return p[1];} return fallback; } // Read a simple query parameter.
    private String value(String body, String key) { String needle="\""+key+"\":\""; int start=body.indexOf(needle)+needle.length(); int end=body.indexOf('\"', start); return start>=needle.length()&&end>start?body.substring(start,end):""; } // Read a simple JSON string field.
    private void write(HttpExchange e, int status, String body) throws IOException { byte[] data=body.getBytes(StandardCharsets.UTF_8); e.getResponseHeaders().set("Content-Type","application/json"); e.sendResponseHeaders(status,data.length); e.getResponseBody().write(data); e.close(); } // Write a JSON HTTP response.
    public static void main(String[] args) throws Exception { WatchlistService service=create(); HttpServer server=service.server(Integer.parseInt(System.getenv().getOrDefault("PORT","8105"))); server.start(); System.out.println("watchlist-service started"); } // Start the service.
}
