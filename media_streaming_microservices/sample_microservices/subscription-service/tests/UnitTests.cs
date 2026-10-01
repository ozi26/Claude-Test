// Unit tests for subscription-service.
using MediaStreamX; // Import the service namespace.
namespace Tests; // Declare the test namespace.
public class UnitTests { // Define unit tests.
    [Fact] public void StoresValue() { var app = new ServiceApp(); app.Subscribe("u1", "premium"); Assert.Equal("premium", app.GetSubscription("u1")); } // Verify service state logic.
}
