import pandas as pd

def loading_data():
    try:
        df = pd.read_excel('data/base_pokemon.xlsx')
        return df
    except FileNotFoundError:
        print("Erro! Arquivo não existe.")
        return None

ordem_geracoes = [
    "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Paldea"
]

def menu():
    df = loading_data()
    df['Regiao'] = pd.Categorical(df['Regiao'], categories=ordem_geracoes, ordered=True)
    
    if df is None or df.empty:
        return

    while True:
        print("\n=== Analisador Pokémon ===")

        print("1- Escolha a geração (ou 'Todas'):")
        chosen_region = input().strip().title()

        region = list(df['Regiao'].unique()) + ["Todas"]
        if chosen_region not in region:
                print(f"Erro: Região inválida! Opções na base: {', '.join(region)}")
                continue

        print("2- Escolha o elemento (ou 'Todos'):")
        chosen_element = input().strip().capitalize()

        tipos_validos = list(df['Tipo'].unique()) + ["Todos"]
        if chosen_element not in tipos_validos:
            print(f"Erro: Elemento não encontrado! Tipos na base: {', '.join(tipos_validos)}")
            continue

        print("3- Escolha o atributo (HP, Ataque, Defesa, Velocidade):")
        chosen_status = input().strip().capitalize()

        if chosen_status == 'Hp' or chosen_status == 'hp':
            chosen_status = 'HP'

        if chosen_status not in ['HP', 'Ataque', 'Defesa', 'Velocidade']:
            print("Atributo inválido!")
            continue

        dados_filtrados = df.copy()

        if chosen_region != "Todas":
            dados_filtrados = dados_filtrados[dados_filtrados['Regiao'] == chosen_region]

        if chosen_element != "Todos":
            dados_filtrados = dados_filtrados[dados_filtrados['Tipo'] == chosen_element]

        if not dados_filtrados.empty:
            print(f"\n--- Resultado da Análise ({chosen_region} / {chosen_element}) ---")

            valor_max = dados_filtrados[chosen_status].max()
            pokemons_max = dados_filtrados[dados_filtrados[chosen_status] == valor_max]['Nome'].tolist()

            valor_min = dados_filtrados[chosen_status].min()
            pokemons_min = dados_filtrados[dados_filtrados[chosen_status] == valor_min]['Nome'].tolist()

            media_geral = dados_filtrados[chosen_status].mean()

            print(f"\nMaior {chosen_status}: {valor_max}")
            print(f"Pokémon(s): {', '.join(pokemons_max)}")

            print(f"\nMenor {chosen_status}: {valor_min}")
            print(f"Pokémon(s): {', '.join(pokemons_min)}")

            print(f"\nMédia Geral de {chosen_status}: {media_geral:.2f}")

            print(f"\n--- Média de {chosen_status} por Região ---")
            media_por_regiao = dados_filtrados.groupby('Regiao')[chosen_status].mean()
            for regiao, media in media_por_regiao.items():
                print(f"{regiao}: {media:.2f}")

        else:
            print("\nNenhum Pokémon encontrado com esses filtros!")

        export = input("\nExportar este resultado para Excel? (S/N): ").strip().upper()
        if export == 'S':
            name_file = f"analise_{chosen_region}_{chosen_element}.xlsx"
            dados_filtrados.to_excel(f"data/{name_file}", index=False)
            print(
                f"✅ Arquivo '{name_file}' gerado com sucesso na pasta 'data'!")

        print("\nDeseja fazer uma nova análise? (S/N)")
        if input().strip().upper() != 'S':
            break

if __name__ == "__main__":
    menu()