// Unit tests for catalog business logic.
const { getMovie, movies } = require('../src/app'); // Import testable catalogue functions.

test('returns an existing movie', () => { // Test successful lookup.
  expect(getMovie('m1')).toEqual(movies[0]); // Confirm the first movie is returned.
}); // End lookup test.

test('returns undefined for an unknown movie', () => { // Test missing lookup behavior.
  expect(getMovie('missing')).toBeUndefined(); // Confirm unknown IDs are rejected.
}); // End missing lookup test.
