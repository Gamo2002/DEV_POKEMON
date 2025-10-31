import pygetwindow as gw
import time

print("Listando todas as janelas abertas em 3 segundos...")
print("Por favor, abra e clique na janela do seu emulador agora.")
time.sleep(3)

try:
    # Pega todas as janelas visíveis
    all_windows = gw.getAllTitles()
    
    print("\n--- TÍTULOS DE JANELAS ENCONTRADOS ---")
    
    if not all_windows:
        print("Nenhuma janela encontrada.")
    else:
        # Filtra títulos vazios e imprime o resto
        for title in all_windows:
            if title: # Ignora strings vazias
                print(f"'{title}'")
    
    print("\n-------------------------------------")
    print("Abra o emulador, encontre o título EXATO na lista acima.")
    print("Copie e cole esse título (incluindo ' ' e símbolos) no seu arquivo 'config.py'.")

except Exception as e:
    print(f"Ocorreu um erro ao tentar listar as janelas: {e}")