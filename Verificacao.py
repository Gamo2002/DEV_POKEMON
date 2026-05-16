
import cv2
from ultralytics import YOLO
# Carrega o arquivo que você baixou do Colab
model = YOLO('best.pt')

# Faz a detecção em uma imagem ou vídeo
results = model.predict(source='P.png', save=False,conf=0.1,imgsz=[736, 1088])
# 4. O YOLO retorna uma lista de resultados. Vamos pegar o primeiro:
res = results[0]

# 5. O método .plot() desenha as caixas e nomes automaticamente na imagem
imagem_com_caixas = res.plot()
# 6. Salva a imagem resultante no seu computador
cv2.imwrite('Achei_o_RED1.jpg', imagem_com_caixas)

print("Sucesso! A imagem 'Achei_o_RED.jpg' foi salva na pasta do projeto.")