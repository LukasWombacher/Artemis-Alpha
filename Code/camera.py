import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><img src="stream.mjpg" width='648' height='486' autoplay playsinline></center>
</body>
</html>
"""
def main():
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = ('192.168.178.45',9000) # Enter your IP address 
    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,2592)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1944)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

def capture_image():
    # Kamera-Objekt initialisieren
    capture = cv2.VideoCapture(0)
    
    # Überprüfen, ob die Kamera erfolgreich geöffnet wurde
    if not capture.isOpened():
        print("Fehler beim Öffnen der Kamera.")
        return
    
    # Bild von der Kamera erfassen
    ret, frame = capture.read()
    
    # Überprüfen, ob das Bild erfolgreich erfasst wurde
    if not ret:
        print("Fehler beim Erfassen des Bildes.")
        return
    
    # Bild im aktuellen Ordner speichern
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    
    # Kamera-Objekt freigeben
    capture.release()
    
    print("Bild erfolgreich erfasst und gespeichert:", image_path)

if __name__=='__main__':
    #main()
    capture_image()
    