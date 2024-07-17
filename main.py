import cv2
import numpy as np

# Função para lidar com o processamento de vídeo e detecção de movimento
def processar_video(captura_de_video):
    último_quadro = None
    sensibilidade = 2000  # Ajustar o limite para detecção de movimento

    while True:
        ret, quadro = captura_de_video.read()

        if not ret:
            print("Erro ao capturar quadro")
            break

        quadro_copia = quadro.copy()

        if último_quadro is None:
            último_quadro = quadro
            continue

        # Calcular diferença de quadro, conversão em escala de cinza e redução de ruído
        diferença = cv2.absdiff(último_quadro, quadro)
        cinza = cv2.cvtColor(diferença, cv2.COLOR_BGR2GRAY)
        borrado = cv2.GaussianBlur(cinza, (7, 7), 0)

        # Limiarização para detectar movimento
        _, limiarizado = cv2.threshold(borrado, 20, 255, cv2.THRESH_BINARY)

        # Encontrar contornos e desenhar caixas delimitadoras para movimento detectado
        contornos, _ = cv2.findContours(limiarizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            if cv2.contourArea(contorno) > sensibilidade:
                (x, y, w, h) = cv2.boundingRect(contorno)
                cv2.rectangle(quadro_copia, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Verde para movimento
                print('Movimento detectado!')
                
                # Destacar o movimento e obscurecer o resto do quadro
                mask = np.zeros_like(quadro)
                cv2.drawContours(mask, [contorno], -1, (255, 255, 255), -1)
                movimento = cv2.bitwise_and(quadro, mask)
                quadro_obscurecido = cv2.addWeighted(quadro, 0.3, movimento, 0.7, 0)

                cv2.imshow('Foco no Movimento', quadro_obscurecido)

        # Exibir quadros
        cv2.imshow('Quadro original', quadro)
        cv2.imshow('Limiarizado', limiarizado)
        cv2.imshow('Com caixas delimitadoras', quadro_copia)

        if cv2.waitKey(1) == ord('q'):
            break

        último_quadro = quadro

# Escolha de vídeo ou webcam
escolha_do_usuário = input("Digite 'v' para usar o arquivo de vídeo ou 'c' para usar a webcam: ")

if escolha_do_usuário == 'v':
    # Abrir arquivo de vídeo
    caminho_do_video = input("Digite o caminho do arquivo de vídeo: ")
    captura_de_video = cv2.VideoCapture(caminho_do_video)
    processar_video(captura_de_video)
elif escolha_do_usuário == 'c':
    # Abrir webcam
    captura_de_video = cv2.VideoCapture(0)
    processar_video(captura_de_video)
else:
    print("Escolha inválida. Por favor, digite 'v' ou 'c'.")

captura_de_video.release()
cv2.destroyAllWindows()


# %%

