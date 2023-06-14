import cv2, time
import  pyshine as ps
import numpy as np


def find_objects():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Fehler beim Öffnen der Kamera.")
        return
    ret, frame = capture.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    cv2.imwrite("bild0.jpg", frame)
    frame = frame[240:250, 1:640] #480
    height, width = frame.shape[0], frame.shape[1]
    print(width)
    frame2 = np.zeros((1, width, 3), np.uint8)
    for i in range(0, width):
        b, g, r = 0, 0, 0
        for j in range(0, height):
            b += frame[j, i][0]
            g += frame[j, i][1]
            r += frame[j, i][2]
        frame2[0, i][0] = b / height
        frame2[0, i][1] = g / height
        frame2[0, i][2] = r / height
    if not ret:
        print("Fehler beim Erfassen des Bildes.")
        return
    cv2.imwrite("bild1.jpg", frame)
    cv2.imwrite("bild2.jpg", frame2)
    #print("Bild erfolgreich erfasst und gespeichert")
    color = [0]*width
    frame3 = np.zeros((1, width, 3), np.uint8)
    for pixel in range(0, width):
        b, g, r = frame2[0, pixel][0], frame2[0, pixel][1], frame2[0, pixel][2]
        if r >= 100 and g <= 80 and b <= 80:
            color[pixel] = "rot"
            frame3[0, pixel] = (0, 0, 255)
        if g >= 30 and r <= 25 and b <= 45:
            color[pixel] = "grün"
            frame3[0, pixel] = (0, 255, 0)
    objects = [[0, 0, 0]]
    in_range = True
    for i in range(0, len(color)):
        if color[i] == "rot" and (i > (objects[-1][1] + (objects[-1][2]/2))):
            j = 1
            while (i+j+1 < len(color)) and (color[i+j] == "rot") and (i > (objects[-1][1] + (objects[-1][2]/2))):
                j += 1
            if j >= 10:
                objects.append(["rot", i+(j/2), j])
        if color[i] == "grün" and (i > (objects[-1][1] + (objects[-1][2]/2))):
            j = 1
            while (i+j+1 < len(color)) and (color[i+j] == "grün") and (i > (objects[-1][1] + (objects[-1][2]/2))):
                j += 1
            if j >= 10:
                objects.append(["grün", i+(j/2), j])
        
    cv2.imwrite("bild3.jpg", frame3)
    #print(objects[1:])
    return objects[:]
    

if __name__=='__main__':
    while True:
        find_objects()
        time.sleep(0.05)
