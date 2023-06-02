# Energie und Sensoren

## Stromversorgung 

Der Raspberry Pi wird von einem passenden Power Hat immer genau mit der benötigten Leistung versorgt. Dieser verfügt über zwei schnell wechselbar Lithium Polymer Akkus die jeweils eine Kapazität von 2700 mAh haben. Sie können direkt über den Power Hat per USB-C oder in eimen externen Ladegerät geladen werden. Vom Raspberry Pi geht eine 5 V ein Ground Kabel zum unter dem Raspberry Pi gelegenen selbstgebauten Stromverteiler, an dem sämtliche Sensoren, Motoren und andere Komponenten, die eine dauerhafte Stromversorgung benötigen angeschlossen sind. Alle Komponenten die kurzzeitig Strom brauche, beispielsweise die Ultraschallsensoren oder der Steppermotor als Signalspannung sind an den GPIO Ports des Raspberry Pi angeschlossen. Um dem Antirebsmotor die vololen 5 V zu gewährleisten ist dieser über einen Transistor per GPIO Pin ansteuerbar.

![20230531_172752](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/7eba4f6c-f6c4-4332-810f-52ad2a33c72a)

![20230531_173150](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/e39160cf-e765-4625-adf2-5f872f94e706)

## Sensoren

Zur Orientierung auf dem SPielfeld und der Erkennung von Hindernissenist das Fahrzeug mit verschiedenen Sensoren ausgestattet.
Zur groben Orientierung sind 3 Ultraschallsensoren verbaut die vorne und an den Seiten angebracht sind. Sie ermöglichen Abstandsmessungen zur Spielfeldbegrenzung.
Des weiteren ist ein Gyroskop und Magnetometer in der Bodenplatte verbaut. Dieser misst kontinuierlich die Rotationsgeschwindigkeit und errchnet daraus seinen Winkel relativ zur Startposition. Dadurch kann in Kurven exakt gelenkt werden und eine perfekte Ausrichtung auf dem Spielfeld wird gewährleistet.
Das Herzstück der Sensoren für das Hindernisrennen ist die Kamera. Sie erkennt Hindernisse, kategorisiert diese nach Farben und errechnet auf Basis der Größe und Abmessungen die Endfernung und Position. Es handelt sich um eine 180° Weitwinkelkamera, dadurch können nicht nur Hindernisse nach vorne, sondern auch noch neben der Kamera erkannt werden. Sie ist außerdem mit Infrarotleuchtmitteln ausgestattet um bei allen Lichtverhältnissen ein klares Bild zu errechnen.

![20230531_172955](https://github.com/LukasWombacher/Artemis-Alpha/assets/109914834/91277caa-cfe3-4a29-a809-8140bc1d091a)

## Teileliste

3x Ultrasonic Sensor Module DC 5V HY-SRF05

1x 3-Achsen-Gyroskop und Beschleunigungssensor MPU-6050

1x Weitwinkelkamera OV5647-Chip
