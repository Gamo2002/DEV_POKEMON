import cv2
import time
from src.screen_capture import capture_game_screen

print("Iniciando IA (Modo de visualização)...")
print("Pressione 'q' na janela 'Game Feed' para parar.")

# Armazena o tempo do último frame para calcular o FPS
last_time = time.time()

# O loop principal da sua IA
while True:
    
    # 1. CAPTURAR (O que estamos fazendo hoje)
    frame = capture_game_screen()
    
    if frame is None:
        print("Erro na captura, encerrando.")
        break

    # 2. PROCESSAR (Próximo passo)
    # (Aqui você vai analisar a 'frame' para encontrar o player, 
    #  ler caixas de diálogo, etc.)
    # ex: game_state = processar_imagem(frame)

    # 3. DECIDIR (O cérebro)
    # (Com base no 'game_state', decidir qual tecla apertar)
    # ex: acao = decidir_acao(game_state)

    # 4. AGIR (O controle)
    # (Simular o pressionamento da tecla 'acao')
    # ex: controlar_input(acao)


    # --- Por enquanto, vamos apenas exibir o feed ---
    
    # Calcula e exibe o FPS (Frames Per Second)
    fps = 1 / (time.time() - last_time)
    last_time = time.time()
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Mostra o feed do jogo em uma janela
    cv2.imshow("Game Feed", frame)

    # Condição de parada (pressionar 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fecha todas as janelas do OpenCV
cv2.destroyAllWindows()
print("Programa finalizado.")