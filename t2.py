import win32gui
import win32ui
import ctypes # Necessário para corrigir o DPI
from ctypes import windll
from PIL import Image

# --- CORREÇÃO 1: DPI Awareness ---
# Isso diz ao Windows: "Não minta para mim sobre o tamanho da tela/janela"
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

def capture_window(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        print(f"Janela '{window_name}' não encontrada.")
        return

    # --- CORREÇÃO 2: Usar GetWindowRect ---
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
    # Se der erro ou ficar preto de novo, tente mudar o 2 para 0.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    if result == 1:
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        # Cria a imagem
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # --- CORREÇÃO 3: Crop Opcional (Remover bordas extras) ---
        # O Windows 10/11 tem bordas invisíveis e sombras que podem vir na captura.
        # Se você quiser SOMENTE o conteúdo interno (sem barra de título), descomente abaixo:
        
        # client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(hwnd)
        # client_point = win32gui.ClientToScreen(hwnd, (0, 0)) # Onde começa a área interna na tela real
        
        # border_thickness = client_point[0] - left
        # title_height = client_point[1] - top
        # img = img.crop((border_thickness, title_height, w - border_thickness, h - border_thickness))

        img.save(f"{window_name}_full.png")
        print(f"Sucesso! Imagem salva: {w}x{h}")
    else:
        print("Falha no PrintWindow.")

    # Limpeza
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

# Teste
capture_window("Calculadora")