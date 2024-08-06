#!/usr/bin/node

const request = require('request');
const { promisify } = require('util');
const requestAsync = promisify(request);

async function getMovieCharacters(movieId) {
  try {
    // Fetch the movie data
    const { body: movieBody } = await requestAsync(`https://swapi-api.hbtn.io/api/films/${movieId}`);
    const { characters } = JSON.parse(movieBody);

    // Fetch character data in parallel
    const characterPromises = characters.map(characterUrl => requestAsync(characterUrl).then(response => JSON.parse(response.body).name));
    const characterNames = await Promise.all(characterPromises);

    // Print character names
    characterNames.forEach(name => console.log(name));

  } catch (err) {
    console.error(err);
  }
}

// Get the Movie ID from command-line arguments and execute the function
const movieId = process.argv[2];
if (movieId) {
  getMovieCharacters(movieId);
} else {
  console.error('Please provide a Movie ID.');
}
