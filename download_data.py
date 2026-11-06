import json
import os
import requests

# Lista inicial de Pokémon para el prototipo (puedes añadir más si quieres)
POKEMON_LIST = [
    "bulbasaur", "ivysaur", "venusaur", 
    "charmander", "charmeleon", "charizard", 
    "squirtle", "wartortle", "blastoise", 
    "pikachu", "raichu", "eevee"
]

def fetch_pokemon_info(name):
    # 1. Datos de tipos, stats y movimientos
    res_poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}").json()
    poke_id = res_poke['id']
    poke_name = res_poke['name'].capitalize()
    types = [t['type']['name'].capitalize() for t in res_poke['types']]
    stats = {s['stat']['name']: s['base_stat'] for s in res_poke['stats']}
    moves = [m['move']['name'].replace('-', ' ').capitalize() for m in res_poke['moves'][:8]]

    # 2. Datos de evolución
    res_species = requests.get(res_poke['species']['url']).json()
    res_evo = requests.get(res_species['evolution_chain']['url']).json()

    evo_details = []
    curr = res_evo['chain']
    while curr:
        species_name = curr['species']['name'].capitalize()
        if curr['evolves_to']:
            for evo in curr['evolves_to']:
                target = evo['species']['name'].capitalize()
                details = evo['evolution_details'][0] if evo['evolution_details'] else {}
                min_level = details.get('min_level')
                item = details.get('item', {}).get('name') if details.get('item') else None
                trigger = details.get('trigger', {}).get('name', 'desconocido')
                
                cond = f"al nivel {min_level}" if min_level else f"usando {item}" if item else f"vía {trigger}"
                evo_details.append(f"{species_name} evoluciona a {target} {cond}.")
            curr = curr['evolves_to'][0]
        else:
            curr = None

    evo_str = " ".join(evo_details) if evo_details else "Este Pokémon no evoluciona."
    tipo_str = " y ".join(types)
    stats_str = f"Atq. Esp: {stats['special-attack']}, Atq: {stats['attack']}, Vel: {stats['speed']}, Def: {stats['defense']}."
    moves_str = ", ".join(moves)

    # Determinar si destaca más en Ataque Físico o Especial
    enfoque = "Ataque Especial" if stats['special-attack'] >= stats['attack'] else "Ataque Físico"

    # Ficha Markdown/Texto que consumirá el RAG
    texto = (
        f"{poke_name} es un Pokémon de tipo {tipo_str}. "
        f"Evolución: {evo_str} "
        f"Stats clave: {stats_str} "
        f"Destaca en {enfoque}. Movimientos destacados: {moves_str}."
    )

    return {
        "id": poke_id,
        "fuente": "pokeapi.co",
        "texto": texto
    }

if __name__ == "__main__":
    print("Descargando datos desde PokéAPI...")
    docs = []
    for name in POKEMON_LIST:
        print(f" - Procesando {name}...")
        docs.append(fetch_pokemon_info(name))
    
    os.makedirs("data", exist_ok=True)
    with open("data/pokemon_data.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)
    print("¡Base documental guardada correctamente en data/pokemon_data.json!")