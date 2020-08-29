from .connection import connect
from .trainer import exists


def type_valid(types_list, connection):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM Type"
        cursor.execute(query)
        types = set([type['name'] for type in cursor.fetchall()])

        return set(types_list).issubset(types)


def is_valid(pokemon,connection):
    if set(pokemon.keys()) == {'id', 'name', 'height', 'weight', 'type'}:
        if type_valid(pokemon['type'], connection):
            #TODO check if valid -owned by
            return True
    return False


def insert_pokemonType(pokemon):
    connection = connect()
    query = "insert into pokemonType values "
    with connection.cursor() as cursor:
        for type in pokemon['type']:
            query += f"({pokemon['id']}, '{type}'),"
        cursor.execute(query[:-1]+';')
    connection.commit()


def insert_pokemon(pokemon):
    connection = connect()
    if is_valid(pokemon, connection):
        with connection.cursor() as cursor:
            try:
                query = f'''INSERT INTO pokemon 
                            VALUES ({pokemon['id']}, 
                                    '{pokemon['name']}', 
                                    {pokemon['height']}, 
                                    {pokemon['weight']});
                        '''
                cursor.execute(query)
            except Exception as e:
                print("string"+str(e))
                if "uplicate" not in str(e).lower():
                    raise e
    else:
        print(pokemon)
        raise ValueError("invalid input")
    connection.commit()


def insert_single_pokemonTrainer(pokemon):
    connection = connect()
    pid = pokemon['id']
    for trainer in pokemon['ownedBy']:
        with connection.cursor() as cursor:
            query = f"insert into pokemonTrainer values ({pid}, '{trainer['name']}');"
            cursor.execute(query)
    connection.commit()


def get_id_by_name(pokemon_name):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
            SELECT id FROM pokemon
            WHERE name = '{pokemon_name}'
        '''
        cursor.execute(query)
    return cursor.fetchone()['id']


def findPokemonByType(type):
    connection = connect()
    if type_valid([type], connection):
        with connection.cursor() as cursor:
            query = f'''SELECT p.name 
                        FROM pokemon p JOIN pokemonType t 
                        ON p.id = t.pid 
                        WHERE t.type = '{type}'''
            cursor.execute(query)
            names = cursor.fetchall()
            return [name['name'] for name in names]


def pokemon_belongs_to_trainer(pid, trainer):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
                SELECT * FROM pokemonTrainer
                WHERE t_name  = '{trainer}' and pid = {pid}
            '''
        cursor.execute(query)
        if not cursor.fetchone():
            return False
        return True


def delete_owners_pokemon_(pname, tname):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''SELECT P.id 
                    FROM pokemon P  
                    WHERE P.name = '{pname}'''''
        cursor.execute(query)
        pid = cursor.fetchone()['id']
        query = f'''DELETE FROM pokemonTrainer 
                    WHERE pid = {pid} and t_name = '{tname}'''''
        cursor.execute(query)
    connection.commit()


def update_pokemonTrainer(pid, new_pid, trainer):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
            UPDATE pokemonTrainer
            SET pid = {new_pid}
            WHERE t_name = '{trainer}' and pid = {pid};
        '''
        cursor.execute(query)
    connection.commit()


def update_data_base(pid, new_name, trainer):
    new_pid = get_id_by_name(new_name)
    update_pokemonTrainer(pid, new_pid, trainer)


def find_pokemon_of_owner(tname):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
               SELECT P.name
                FROM pokemon P JOIN pokemonTrainer PT
                ON P.id = PT.pid
                WHERE '{tname}' = PT.t_name
           '''
        cursor.execute(query)
        return cursor.fetchall()[0]['name']


def evolve(pid, pname, evolve_to, trainer):
    if not exists(trainer):
        raise ValueError("Trainer not found.")

    if not pokemon_belongs_to_trainer(pid, trainer):
        raise ValueError(f"Trainer {trainer} does not train pokemon {pname}.")

    update_data_base(pid, evolve_to, trainer)


def pokemons_to_adopt():
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
                    SELECT P.name as NAME, P.id as ID, P.weight as WEIGHT, P.height as HEIGHT
                    FROM pokemon P 
                    WHERE NOT EXISTS (SELECT pid
                                        FROM pokemonTrainer
                                        WHERE P.id = pid)
                   '''
        cursor.execute(query)
        return cursor.fetchall()


def adopt(pid, tname):
    connection = connect()
    with connection.cursor() as cursor:
        query = f'''
               INSERT INTO pokemonTrainer
                VALUES ({pid},'{tname}');
           '''
        cursor.execute(query)
    connection.commit()

