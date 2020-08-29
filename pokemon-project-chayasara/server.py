from flask import Flask, Response, request, render_template
from models import pokemon as pokemon_file, trainer as trainer_file
import pokeAPI

app = Flask(__name__, static_url_path='', static_folder='public')


@app.route('/pokemons', methods=["POST"])
def insert_pokemon():
    pokemon = request.get_json()
    try:
        pokemon_file.insert_pokemon(pokemon)
        pokemon_file.insert_pokemonType(pokemon)
    except ValueError as v:
        return {"error": f"pokemon was not inserted, {v}"}, 400

    except Exception as e:
        if "duplicate" in str(e).lower():
            return {"status": "pokemon inserted successfully"}, 202
        return {"pokemon wasn't inserted": str(e)}, 500

    return Response({"status": "pokemon inserted successfully"}), 201


@app.route('/pokemons/<type>')  # if more gets will be added in future, use query params
def get_pokemon_by_type(type):
    result = pokemon_file.findPokemonByType(type)
    return {"result": result}, 200


@app.route('/pokemons', methods=["DELETE"])
def delete_owners_pokemon():
    to_delete = request.get_json()
    try:
        pokemon_file.delete_owners_pokemon_(to_delete['pname'], to_delete['tname'])

    except:
        return {"error": "couldn't delete"}, 400
    return {"status": "deleted"}, 200


@app.route('/pokemons/evolve/<trainer>/<pokemon_name>', methods=["PUT"])
def evolve(trainer, pokemon_name):
    print("here")
    try:
        pid = pokemon_file.get_id_by_name(pokemon_name)
    except:
        return {"error": "pokemon doesn't exist"}, 404

    try:
        evolve_to = pokeAPI.evolve_to(pokemon_name)
        if not evolve_to:
            return {"error": f"pokemon {pokemon_name} is fully evolved"}, 400

    except Exception as e:
        return {"error": f"{e}"}, 500

    try:
        pokemon_file.evolve(pid, pokemon_name, evolve_to, trainer)
    except Exception as e:
        return {"error": f"{e}"}, 400

    return {"status": f"pokemon {pokemon_name} was evolved to {evolve_to}"}, 205


# ================Extension========================

@app.route("/pokemons/news")
def header():
    return app.send_static_file("adopt_add.pdf")


@app.route("/pokemons/adopt")
def adopt():
    list = pokemon_file.pokemons_to_adopt()
    columnNames = ["NAME", "ID", "HEIGHT", "WEIGHT"]
    return render_template('pokemon_to_adopt.html', records=list, colnames=columnNames)


@app.route("/pokemons/adopt_by_id")
def adopt_by_id():
    if not ((request.args.get('pid')) or (request.args.get('trainer'))):
        return {"error": "missing params!!"}

    pid = request.args.get('pid')
    print(pid)
    tname = request.args.get('trainer')
    print(tname)
    if not trainer_file.exists(tname):
        return {"error": "Trainer does not exist!!"}, 400
    pname = pokemon_file.find_pokemon_of_owner(tname)
    pokemon_file.adopt(pid, tname)
    evolve(tname, pname)
    return app.send_static_file("congratulations.JPEG.jpg")


if __name__ == '__main__':
    # setupDatabase()
    app.run(port=3000)
