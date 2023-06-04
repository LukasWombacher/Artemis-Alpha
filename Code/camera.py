import cv2, time
import  pyshine as ps
import numpy as np

def capture_image():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Fehler beim Öffnen der Kamera.")
        return
    ret, frame = capture.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = frame[250:260, 0:640] #480
    height = 1
    width = 640
    frame2 = np.zeros((height,width,3), np.uint8)
    for i in range(0, 640):
        for j in range(0, 10):
            frame2[0, i] += frame[j, i]
        frame2[0, i] /= 10
    dimensions = frame2.shape
    print(dimensions)
    if not ret:
        print("Fehler beim Erfassen des Bildes.")
        return
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame2)
    print("Bild erfolgreich erfasst und gespeichert:", image_path)

if __name__=='__main__':
    #main()
    while True:
        capture_image()
        time.sleep(0.05)
    