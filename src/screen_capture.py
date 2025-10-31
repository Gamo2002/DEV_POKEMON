import numpy as np
import mss
import cv2

# Inicializa o mss uma vez só
sct = mss.mss()

def capture_game_screen(window_obj):
    """
    Captura a tela usando um objeto de janela fornecido pelo pygetwindow.
    Esta função obtém as coordenadas mais recentes da janela a cada chamada.
    """
    try:
        # 1. Verifica se a janela ainda existe e está visível
        if window_obj is None or not window_obj.visible or window_obj.isMinimized:
            print("Aviso: Janela alvo não está visível ou foi fechada.", end="\r")
            return None

        # 2. Pega as coordenadas ATUAIS da janela
        # Esta é a "mágica": o objeto se atualiza se você mover a janela!
        coords = {
            "top": window_obj.top,
            "left": window_obj.left,
            "width": window_obj.width,
            "height": window_obj.height
        }

        # 3. Garante que a janela tenha um tamanho válido para captura
        if coords["width"] <= 0 or coords["height"] <= 0:
            print("Aviso: Janela com tamanho inválido (0 pixels).", end="\r")
            return None

        # 4. Captura usando as coordenadas
        sct_img = sct.grab(coords)
        
        # 5. Converte para o formato OpenCV
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img_bgr
        
    except mss.exception.ScreenShotError:
        # A janela pode ter sido fechada no exato momento da captura
        print("Erro de captura (ScreenShotError). A janela foi fechada?", end="\r")
        return None
    except Exception as e:
        # Outros erros (ex: pygetwindow pode falhar se a janela for fechada)
        print(f"Erro inesperado na captura: {e}", end="\r")
        return None