# Motorisierung

## Fahrzeugaufbau

Alle Konstruktionsteile des Fahrzeugs sind selbst designt und 3D gedruckt. Die Basis bildet dabei den Mittelteil, das ergänzt wird durch die Getriebehalterung, die Einzelteile der Lenkung und sämtliche kleineren Anbauteile. Die wichtigsten CAD-Modelle für einen groben Überblick über Aufbau und Struktur des Fahrzeugs liegen hier im Motorisierungsordner. Alle weiteren Modelle, die für den Bau das Notwendig sind, sind im CAD-Modelle Ordner zu finden.

![image](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/b1f73249-6c25-4832-bdc7-99efc5357404)


## Antriebsmotor

Das Fahrzeug wird angetrieben durch einen N20 Getriebemotor mit 200 RPM (Umdrehungen pro Minute) der mit 5V betrieben wird. Auf diesen ist ein selbstgedrucktes Zahnrad geschraubt, dass die Drehbewegung nach unten auf ein Differenzialgetriebe überträgt. Das Differenzialgetriebe ist direkt mit den Rädern verbunden. Durch die Übersetzung, Reibungsverluste und sonstige Faktoren beschleunigt er das Fahrzeug auf eine Geschwindigkeit von bis zu x m/s. Ein automatisches Umschalten auf geringere Geschwindigkeiten ist durch Spannungsänderung möglich. Wir haben uns bewusst gegen einen deutlich stärkeren 12 V Motor entschieden, weil diese deutlich schwerer sind und der zusätzliche 12 V Akku zusätzlichen Platz einnehmen würde, was unserer Strategie eines möglichst kompakten wendigen Fahrzeugs widersprechen würde.

![20230531_173038](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/0ae8a8e7-ed3b-4b8c-852d-6cf404498b3c)


## Lenkmotor

Wir haben uns dazu entschieden Lenk- und Antriebsachse zu trennen, da eine gemeinsame Achse nicht nur deutlich komplexer, sondern auch fehleranfälliger wäre. Dafür hat unsere Lenkachse, die vorne angebracht ist, einen Lenkwinkel von 60° der es ermöglicht Kreise mit 15 cm Innen- und 45 cm Außendurchmesser zu fahren. Auch die Lenkung ist selbst entworfen und gedruckt. Es handelt sich dabei um eine Motorstange, die die Lenkbewegung auf die Lenkstange überträgt, an der die Räder aufgehängt sind und auf der Stelle drehen. Der Lenkmotor ist dabei ein 5 V Steppermotor mit 4 Spulen (28BYJ-48 ULN2003) der von einem Motorcontroller gesteuert wird.

![20230531_173239](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/c10c089d-09d8-48b9-9de9-54c4402eea0c)

![20230531_173330](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/42acc687-df6e-475d-b9f8-5ea88ab64d01)
