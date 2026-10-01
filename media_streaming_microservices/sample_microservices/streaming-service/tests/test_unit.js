// Unit tests for streaming session creation.
const { createPlaybackSession } = require('../src/app'); // Import the business function.

test('creates a playback session', () => { // Test valid input.
  const result = createPlaybackSession('u1', 'm1'); // Create a sample session.
  expect(result.userId).toBe('u1'); // Verify user ID.
  expect(result.mediaId).toBe('m1'); // Verify media ID.
  expect(result.playbackUrl).toContain('m1'); // Verify the media appears in the URL.
}); // End valid input test.

test('rejects missing user', () => { // Test validation.
  expect(() => createPlaybackSession('', 'm1')).toThrow(); // Confirm missing user is rejected.
}); // End validation test.
