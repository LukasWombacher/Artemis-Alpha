# Hindernisse

## Wann werden Hindernisse erkannt?

Die Hindernisse stehen nur auf den Geraden Abschnitten. Darum beginnt deren Erkennung unmittelbar nachdem die Kurve gefahren wurde.
Das Hindernis-Programm basiert auf dem Eröffnungsrennen-Programm. Die Kurve wird jedoch frühzeitig beendet und von der Geradenkorrektur weitergeführt, damit auch Hindernisse direkt am Anfang des Abschnitts berücksichtigt werden können.

## Wie werden sie erkannt?

Wie bereits oben erwähnnt ist die Hinderniserkennung Teil der Geradenkorrektur. Die 180° Kamera nimmt in jeder Wiederholung der Schleife ein Bild auf. Das Bild wird zuerst auf einen Pixelstreifen (horizontal) der Breite 10 reduziert, um die Datenmenge zu reduzieren und nicht relevante Bereiche auszublenden. Amschließend werden die 10 übereinanderliegenden Pixel zu einem Durchschnittspixel zusammengefasst, sodass sich ein Streifen von einem Pixel Höhe ergibt. In diesem Farbstreifen werden die einzelnen Pixel analysiert und in die Kategorien grün, rot und ungültig eingeteilt. Befinden sich viele rote oder grüne Pixel nebeneinander, wird dieser Bereich als Hinderniss klassifiziert. Das Hinderniss bekommt eine Farbe, eine x-Position, einen Eindeutigkeitswert, und eine Breite zugewiesen.

## Wie wird darauf reagiert?

Anhand der Breite wird eine ungefähre Entfernung errechnet. Dann wird das am nächsten gelegene Hinderniss ausgewählt. Anhand der x-Position und der aktuellen Drehung der Gyroskops wird der benötigte Lenkwinkel berechnet. Die Lenkgeschwindigkeit ist abhängig von der Entfernung und die Lenkrichtung abhängig von der Farbe.

Dieser Ablauf wird auf der ganzen Gerade wiederholt, solange Hindernisse vorhanden sind. Ansonsten greift die Gyroskop-basierte Geradenkorrektur aus dem Eröffnungsrennen.

## Struktogramm

![image](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/221009e4-3d8c-4f53-8889-8147fb06ec0a)
