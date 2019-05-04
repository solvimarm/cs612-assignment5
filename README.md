# cs612-assignment5

## Pokedex API
Hardcoded json data file containing information from the pokedex about the original 151 pokemon.

#### Routes

- /pokedex
  - returns the entire pokedex
- /pokedex/pokemon/<ID>
  - returns all the information the pokedex contains for the pokemon with the corresponding ID
- /pokedex/getAllTypes
  - returns a list of all pokemon elemental types 
- /pokedex/getPokemonByType/<elemental type>
  - returns a list of all pokemon that have the corresponding elemental type
- /pokedex/getEvolutions/<pokemon (either name or ID)>
  - returns previous and next evolution of a pokemon, if applicable

## Running in Docker
docker build -t pokedex .
docker run -p 5000:5000 pokedex