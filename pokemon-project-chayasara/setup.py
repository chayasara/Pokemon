import pymysql
import json
from models import pokemon as pokemon_file

with open("pokemon_data.json") as file:
    data = json.load(file)

def connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        db="pokemon",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_trainers():
    owners_set = set()
    connection = connect()
    for owner_list in [pokemon['ownedBy'] for pokemon in data]:
        for owner in owner_list:

            if owner['name'] not in owners_set:
                owners_set.add(owner['name'])
                entry = {'name': owner['name'], 'town': owner['town']}
                with connection.cursor() as cursor:
                    try:
                        insert_trainer = f"insert into trainer values ('{entry['name']}', '{entry['town']}');"
                        cursor.execute(insert_trainer)
                    except Exception as e:
                        print("string" + str(e))
                        if "uplicate" not in str(e).lower():
                            raise e
    connection.commit()


def insert_pokemons_from_data():
    for pokemon in data:
        pokemon_file.insert_pokemon(pokemon)


def insert_pokemonType_from_data():
    for pokemon in data:
        pokemon_file.insert_pokemonType(pokemon)

def insert_pokemonTrainer():
    for pokemon in data:
        pokemon_file.insert_single_pokemonTrainer(pokemon)



def setupDatabase():
    insert_trainers()
    insert_pokemons_from_data()
    insert_pokemonType_from_data()
    insert_pokemonTrainer()
    print("Welcome to the Pokemon!!!")

