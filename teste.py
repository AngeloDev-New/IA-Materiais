# !pip install opencv-contrib-python --force-reinstall

from ultralytics import YOLO
import cv2

# Carrega o modelo (troque pelo seu .pt se quiser)
model = YOLO("yolo11n.pt")

# Abre a webcam (0 = webcam padrão)
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Faz inferência
    results = model(frame, conf=0.4, verbose=False)

    # Mostra resultado com bounding boxes
    annotated = results[0].plot()
    cv2.imshow("YOLO Webcam", annotated)

    # Aperte 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
