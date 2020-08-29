import pokeAPI
from models import pokemon


for i in range(20):
    new_pokemon = pokeAPI.get_new_poke(i+200)
    pokemon.insert_pokemon(new_pokemon)
    pokemon.insert_pokemonType(new_pokemon)
    print(new_pokemon, "inserted")