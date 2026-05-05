import requests
import pandas as pd
import os

regions_limits = {
    "Kanto": (1, 151),
    "Johto": (152, 251),
    "Hoenn": (252, 386),
    "Sinnoh": (387, 493),
    "Unova": (494, 649),
    "Kalos": (650, 721),
    "Alola": (722, 809),
    "Galar": (810, 905),
    "Paldea": (906, 1025),
    "Todas": (1, 1025)
}

def id_region(id_pokemon):
    match id_pokemon:
        case id if id <= 151:
            return "Kanto", "1ª Geração"
        case id if id <= 251:
            return "Johto", "2ª Geração"
        case id if id <= 386:
            return "Hoenn", "3ª Geração"
        case id if id <= 493:
            return "Sinnoh", "4ª Geração"
        case id if id <= 649:
            return "Unova", "5ª Geração"
        case id if id <= 721:
            return "Kalos", "6ª Geração"
        case id if id <= 809:
            return "Alola", "7ª Geração"
        case id if id <= 905:
            return "Galar", "8ª Geração"
        case _:
            return "Paldea", "9ª Geração"

def extract_data(choice="Todas"):
    pokemons = []
    ## choice = input("Qual será a região?").capitalize()

    if choice in regions_limits:
        start, end = regions_limits[choice]
    else:
        print("Região inválida! Usando 'Todas' por padrão.")
        start, end = regions_limits["Todas"]

    for i in range(start, end + 1):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            regiao, geracao = id_region(data["id"])
            
            pokemon = {
                "Nome": data["name"].capitalize(),
                "ID": data["id"],
                "Geracao": geracao,
                "Regiao": regiao,
                "Tipo": data["types"][0]["type"]["name"].capitalize(),
                "HP": data["stats"][0]["base_stat"],
                "Ataque": data["stats"][1]["base_stat"],
                "Defesa": data["stats"][2]["base_stat"],
                "Velocidade": data["stats"][5]["base_stat"]
            }
            
            pokemons.append(pokemon)
            print(f"Item {i}: Pokémon {pokemon['Nome']} catalogado!")
    
    df = pd.DataFrame(pokemons)

    ## if not os.path.exists("data"):
        ## os.makedirs("data")

    df.to_excel("data/base_pokemon.xlsx", index=False)
    print("Sucesso! O 'Estoque' de dados foi atualizado em data/base_pokemon.xlsx")

if __name__ == "__main__":
    extract_data()