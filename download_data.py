import json
import os
import requests

# Descargaremos los primeros 151 Pokémon (Primera Generación)
START_ID = 1
END_ID = 151

def fetch_pokemon_by_id(poke_id):
    try:
        # 1. Datos del Pokémon (stats, tipos y movimientos)
        res_poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}").json()
        poke_name = res_poke['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in res_poke['types']]
        stats = {s['stat']['name']: s['base_stat'] for s in res_poke['stats']}
        moves = [m['move']['name'].replace('-', ' ').title() for m in res_poke['moves'][:6]]

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
                    trigger = details.get('trigger', {}).get('name', 'unknown method')
                    
                    if item:
                        item_name = item.replace('-', ' ').title()
                        cond = f"using a {item_name}"
                    elif min_level:
                        cond = f"at level {min_level}"
                    else:
                        cond = f"via {trigger}"
                        
                    evo_details.append(f"{species_name} evolves into {target} {cond}.")
                curr = curr['evolves_to'][0]
            else:
                curr = None

        evo_str = " ".join(evo_details) if evo_details else "This Pokemon does not evolve."
        tipo_str = " and ".join(types)
        stats_str = f"Sp. Atk: {stats['special-attack']}, Atk: {stats['attack']}, Speed: {stats['speed']}, Def: {stats['defense']}."
        moves_str = ", ".join(moves)

        enfoque = "Special Attack" if stats['special-attack'] >= stats['attack'] else "Physical Attack"

        texto = (
            f"{poke_name} is a {tipo_str}-type Pokemon. "
            f"Evolution: {evo_str} "
            f"Key stats: {stats_str} "
            f"Focuses on {enfoque}. Notable moves: {moves_str}."
        )

        return {
            "id": poke_id,
            "fuente": "pokeapi.co",
            "texto": texto
        }
    except Exception as e:
        print(f"Error fetching ID {poke_id}: {e}")
        return None

if __name__ == "__main__":
    print(f"Downloading data for Pokemon 1 to {END_ID} from PokéAPI...")
    docs = []
    
    for poke_id in range(START_ID, END_ID + 1):
        doc = fetch_pokemon_by_id(poke_id)
        if doc:
            docs.append(doc)
            print(f"[{poke_id}/{END_ID}] Downloaded: {doc['texto'].split('.')[0]}")
    
    os.makedirs("data", exist_ok=True)
    with open("data/pokemon_data.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)
        
    print(f"\nFinished! {len(docs)} documents saved to data/pokemon_data.json")