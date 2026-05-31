import cv2
import time
import pygetwindow as gw
from src.screen_capture import capture_game_screen
from config import GAME_FEED_TITLE

def select_target_window():
    """
    Mostra uma lista de janelas abertas para o usuário escolher
    e retorna o objeto da janela escolhida.
    """
    print("Procurando janelas disponíveis...")
    valid_windows = []
    
    try:
        # Pega todas as janelas
        all_windows = gw.getAllWindows()
        
        for window in all_windows:
            # Filtra janelas que não queremos:
            # 1. Sem título
            # 2. A nossa própria janela de feed
            # 3. Minimizadas
            if (window.title and 
                GAME_FEED_TITLE not in window.title and 
                not window.isMinimized):
                
                valid_windows.append(window)

        if not valid_windows:
            print("\nERRO: Nenhuma janela válida encontrada.")
            print("Verifique se o seu emulador está aberto e não está minimizado.")
            return None

        # Mostra a lista para o usuário
        print("\n--- Por favor, selecione a janela do jogo ---")
        for i, window in enumerate(valid_windows):
            print(f"  [{i+1}] {window.title}  (Tamanho: {window.width}x{window.height})")

        # Loop para pegar a escolha do usuário
        while True:
            try:
                choice = input(f"\nDigite o número (1-{len(valid_windows)}): ")
                choice_int = int(choice) - 1 # Converte para índice (base 0)
                
                # Valida a escolha
                if 0 <= choice_int < len(valid_windows):
                    chosen_window = valid_windows[choice_int]
                    print(f"\n[SUCESSO] Mira travada na janela: '{chosen_window.title}'")
                    return chosen_window
                else:
                    print(f"Erro: Por favor, digite um número entre 1 e {len(valid_windows)}.")
            except ValueError:
                print("Erro: Por favor, digite apenas o número.")

    except Exception as e:
        print(f"Ocorreu um erro ao listar as janelas: {e}")
        return None

# --- Início do Programa Principal ---

# 1. Deixa o usuário escolher a janela
target_window = select_target_window()

if target_window is None:
    print("Nenhuma janela selecionada. Encerrando o programa.")
    exit() # Encerra o script

# Se deu tudo certo, continua...
print(f"Iniciando captura. Pressione 'q' na janela '{GAME_FEED_TITLE}' para parar.")
last_time = time.time()

# 2. Loop principal
while True:
    
    # 1. CAPTURAR (passando o objeto da janela escolhida)
    frame = capture_game_screen(target_window)
    
    if frame is None:
        # Se a janela foi fechada, 'frame' será None
        print("\nAviso: A janela de captura foi perdida (fechada?). Encerrando...")
        break # Sai do loop

    # --- O resto do código continua igual ---
    fps = 1 / (time.time() - last_time)
    last_time = time.time()
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow(GAME_FEED_TITLE, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza final
cv2.destroyAllWindows()
print("\nPrograma finalizado.")