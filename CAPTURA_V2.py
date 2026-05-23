import win32gui
import win32ui
import ctypes # Necessário para corrigir o DPI
from ctypes import windll
from PIL import Image
import pygetwindow as gw
import cv2
import numpy as np

# --- CORREÇÃO 1: DPI Awareness ---
# Pega o tamanho real da tela/janela"
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

def capture_window(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        print(f"Janela '{window_name}' não encontrada.")
        return

    # PrintWindow captura a janela inteira (com bordas e título),
    # então precisamos criar um bitmap do tamanho total, não só da área interna.
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top

    # Setup do Contexto de Dispositivo (DC)
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    # Captura (Flag 2 = PW_RENDERFULLCONTENT para janelas modernas/Chrome/Apps)
    # Se der erro ou ficar preto mudar o 2 para 0.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    if result == 1:
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        # Cria a imagem (Parte não otimizada, muito recuso para salvar, perdemos desempenho)
        # img = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),bmpstr, 'raw', 'BGRX', 0, 1)
        # img.save(f"P.png")

        # 2. Pula o PIL/Pillow! (Não converte mais para o python) Manda a tinta direto para a biblioteca matemática (Numpy)
        # Aqui criamos um array de 1 dimensão com todos os pixels misturados
        img_array = np.frombuffer(bmpstr, dtype=np.uint8)
        # 3. Molda o array para o formato do OpenCV: (Altura, Largura, Canais de Cor)
        # O Windows retorna 4 canais de cor: Azul, Verde, Vermelho e Transparência (BGRA)
        img_array.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
        # 4. Remove o canal de transparência (A) porque a IA não precisa dele
        # O OpenCV trabalha por padrão com BGR (3 canais)
        img_final = img_array[:, :, :3] 
        
        # Exemplo: Mostrando a imagem na tela em tempo real só para você testar
        cv2.imshow("Visão da IA (Direto da RAM)", img_final)
        cv2.waitKey(1) # Necessário para o cv2 conseguir atualizar a janela
        print(f"Sucesso! Imagem salva: {w}x{h}")
    else:
        print("Falha no PrintWindow.")

    # Limpeza
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

def listar_janelas():
    # listar janelas basicamente pega todas as janelas abertas 
    janelasabertas = []

    def callback(hwnd, _):
        # esse if verifica se é uma janela visivel
        if win32gui.IsWindowVisible(hwnd):
            # pega o nome da janela - hwnd é o id da janela
            titulo = win32gui.GetWindowText(hwnd)
            if titulo:
                # verifica se o nome não é vazio e salva em janelas abertas
                janelasabertas.append(titulo)
    # chama a função callback e fazendo tipo um for passando por todas as janelas abertas do sistema
    win32gui.EnumWindows(callback, None)
    return janelasabertas

# Executa - um em cada retorno do listar janelas e depois compara se tem a palavra "visualboy" joga em janelacerta
for titulo in listar_janelas():
    if "visualboy" in titulo.lower():
        # se tem a palavra executa a função de capturar a imagem.
        janelacerta = titulo
        # capture_window(titulo)

while True:
    frame = capture_window(janelacerta)
    if frame is not None:
        cv2.imshow("Pokemon AO VIVO",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpeza final
cv2.destroyAllWindows()