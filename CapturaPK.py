import win32gui
import win32ui
import ctypes
from ctypes import windll
import numpy as np
import cv2
from ultralytics import YOLO

# --- CONFIGURAÇÃO INICIAL ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

model = YOLO('best.pt')

# --- FUNÇÕES ---

def achar_janela(palavra_chave):
    janelasabertas = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            titulo = win32gui.GetWindowText(hwnd)
            if titulo:
                janelasabertas.append(titulo)
                
    win32gui.EnumWindows(callback, None)

    for titulo in janelasabertas:
        # lower() deixa tudo minúsculo para facilitar a busca
        if palavra_chave.lower() in titulo.lower():
            return titulo
            
    return None # Retorna vazio se não achar

def setup_captura(window_name):
    # """Prepara a 'Tela' (DC) e o 'Papel' (Bitmap) na memória. Roda 1 vez."""
    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        return None
    # descobre o tamanho da janela
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top
    # monta 
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    # monta a tela em branco onde vai ser copiado da janela 
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    
    # Precisamos retornar TUDO para poder limpar depois
    return hwnd, hwndDC, mfcDC, saveDC, saveBitMap, w, h

def capturar_frame(hwnd, saveDC, saveBitMap, w, h):
    # """Bate a foto e devolve a matriz do OpenCV (CV2). Roda a cada frame."""
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    if result == 1:
        bmpstr = saveBitMap.GetBitmapBits(True)
        img_array = np.frombuffer(bmpstr, dtype=np.uint8)
        img_array.shape = (h, w, 4)
        
        # Remove o canal Alpha e retorna o frame pronto (BGR)
        img_final = img_array[:, :, :3] 
        return img_final
    else:
        return None

def limpar_memoria(hwnd, hwndDC, mfcDC, saveDC, saveBitMap):
    # """Destrói os recursos na memória RAM nativa do Windows."""
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


# --- LOOP PRINCIPAL  ---

if __name__ == "__main__":
    
    # 1. Encontra o emulador
    janela_alvo = achar_janela("visualboy")
    
    if not janela_alvo:
        print("Emulador não encontrado! Abra o jogo primeiro.")
    else:
        print(f"Acoplado à janela: {janela_alvo}")
        
        # 2. Monta as ferramentas UMA única vez
        recursos = setup_captura(janela_alvo)
        
        if recursos:
            # Desempacota a tupla retornada pela função
            hwnd, hwndDC, mfcDC, saveDC, saveBitMap, w, h = recursos
            
            print("Pressione 'q' na janela do OpenCV para encerrar.")
            
            try:
                # 3. O Loop Infinito (O Jogo)
                while True:
                    frame = capturar_frame(hwnd, saveDC, saveBitMap, w, h)
                    
                    if frame is not None:
                        results = model.predict(source=frame, save=False,conf=0.1,imgsz=[736, 1088],stream=True, verbose=False)
                        for res in results:     
                            imagem_com_caixas = res.plot()                
                            cv2.imshow("Visao da IA", imagem_com_caixas)
                        
                    # Pausa de 1ms e verifica se apertou 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                        
            finally:
                # 4. Limpeza Garantida (Executa mesmo se o código der erro/crash)
                limpar_memoria(hwnd, hwndDC, mfcDC, saveDC, saveBitMap)
                cv2.destroyAllWindows()
                print("Recursos liberados com sucesso.")