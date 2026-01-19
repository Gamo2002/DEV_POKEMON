import win32gui
import win32ui
from ctypes import windll
from PIL import Image

# 1. Encontrar o 'handle' da janela (ex: "Calculadora")
# Use win32gui.FindWindow(None, "Nome da Janela Exato")
hwnd = win32gui.FindWindow(None, "Calculadora") # Substitua pelo título da sua janela

if hwnd:
    # 2. Obter as dimensões da janela
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bottom - top

    # 3. Capturar a janela específica (usando a API do Windows)
    # Isso requer um contexto de dispositivo (DC)
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    # Copiar a imagem da janela para o bitmap
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    if result == 1:
        # 4. Salvar ou exibir a imagem (exemplo com PIL)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        
        img.save("captura_janela.png")
        print("Captura salva como 'captura_janela.png'")
    else:
        print("Falha ao capturar a janela.")

    # 5. Limpar os recursos
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

else:
    print("Janela não encontrada. Verifique o título exato.")

