import requests


def get_chain(pname):
    url = f"https://pokeapi.co/api/v2/pokemon/{pname}"
    species_url = requests.get(url=url, verify=False).json()['species']['url']
    evolution_chain_url = requests.get(url=species_url, verify=False).json()['evolution_chain']['url']
    return requests.get(url=evolution_chain_url, verify=False).json()['chain']

def evolve_to(pname):
    chain = get_chain(pname)

    while 'species' not in chain:
        chain = chain['evolves_to'][0]

    while chain['species']['name'] != pname:
        chain = chain['evolves_to'][0]

    if not chain.get('evolves_to'):
        print("here")
        return None

    new_name = chain['evolves_to'][0]['species']['name']
    return new_name
#=====================================================


def get_new_poke(id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    print("here")

    details = requests.get(url=url, verify=False).json()
    new_poke = {}
    new_poke['name'] = details['forms'][0]['name']
    new_poke['id'] = id
    new_poke['height'] = details['height']
    new_poke['weight'] = details['weight']
    list = [details['types'][i]['type']['name'] for i in range (len(details['types']))]
    new_poke['type'] = list
    return new_poke
