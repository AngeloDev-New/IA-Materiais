from ultralytics import YOLO
import cv2

class Camera:
    def __init__(self, link,direction,distancia,model = "yolo11n.pt"):
        self.model = YOLO(model)
        self.link = link
        self.cap = cv2.VideoCapture(link)

    def __del__(self):
        self.release()
        cv2.destroyAllWindows()



    def get_frame(self,recise = None):
        if not self.cap.isOpened():
            raise Exception("Não consegui abrir o stream")

        ret, frame = self.cap.read()
        if recise:
            frame = cv2.resize(frame, recise)
        if not ret:
            raise Exception("Não consegui capturar frame")
        return frame

    def release(self):
        self.cap.release()
    def testPredict(self):
        while True:
            frame = self.get_frame((800,600))

            # roda YOLO em um único frame
            results = self.model.track(frame, persist=True)

            # desenha bounding boxes no frame
            annotated = results[0].plot()

            cv2.imshow("YOLO Stream", annotated)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    linkStream = 'https://video04.logicahost.com.br/portovelhomamore/fozpontedaamizadesentidoparaguai.stream/playlist.m3u8'
    local = {'lat': -25.50949500, 'lng': -54.599215, 'nome': 'ponte_aduana'}
    direction = 270
    distancia = 500
    cam = Camera(linkStream,direction,distancia,modelo = 'yolo11n.pt')
    cam.testPredict()

