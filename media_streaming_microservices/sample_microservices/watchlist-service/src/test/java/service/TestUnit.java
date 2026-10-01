package service; // Declare the test package.

import org.junit.jupiter.api.Test; // Import JUnit's test annotation.
import static org.junit.jupiter.api.Assertions.*; // Import assertion helpers.
import java.util.List; // Import list support.

class TestUnit { // Define unit tests for watchlist-service.
    @Test void storesMedia() { WatchlistService service=WatchlistService.create(); service.add("u1","m1"); assertEquals(List.of("m1"), service.list("u1")); } // Verify in-memory storage.
}
