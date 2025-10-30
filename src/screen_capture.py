import numpy as np
import mss
import cv2

# --- IMPORTANTE: Defina a Região de Captura ---
# Você precisará ajustar essas coordenadas para que correspondam
# exatamente à janela do seu emulador Pokémon.
# (top, left) é o canto superior esquerdo.
# Use um print screen e o Paint/GIMP para achar os pixels.
GAME_WINDOW_COORDS = {"top": 100, "left": 100, "width": 640, "height": 480}
# ------------------------------------------------

# Inicializa o objeto de captura de tela (mss)
# Fazer isso fora da função é mais eficiente
sct = mss.mss()

def capture_game_screen():
    """
    Captura a região da janela do jogo e a retorna como um 
    array numpy compatível com OpenCV (BGR).
    """
    try:
        # Captura a tela usando as coordenadas
        sct_img = sct.grab(GAME_WINDOW_COORDS)
        
        # Converte a imagem bruta (BGRA) para um array numpy
        img = np.array(sct_img)
        
        # O mss captura em formato BGRA. O OpenCV geralmente usa BGR.
        # Vamos converter de BGRA para BGR (removendo o canal Alpha/transparência)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img_bgr

    except mss.exception.ScreenShotError:
        print("Erro: Coordenadas de captura fora da tela.")
        return None

# Bloco para testar este módulo de forma independente
if __name__ == '__main_':
    print("Iniciando teste de captura... Pressione 'q' na janela para sair.")
    
    while True:
        frame = capture_game_screen()
        
        if frame is not None:
            # Mostra a imagem capturada em uma janela
            cv2.imshow("Teste de Captura", frame)
        
        # Condição de parada: pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()
    print("Teste finalizado.")