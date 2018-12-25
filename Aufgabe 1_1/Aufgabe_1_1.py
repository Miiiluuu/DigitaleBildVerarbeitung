"""
    Aufgabe 1.1:
    Darstellung eines aufgenommenen Szintigramms, bestehend aus 256x256 Pixel,
    aufgebaut aus vier Flaechenquellen (weitere Parameter siehe Vorlesung zu
    Modul MF-MRS_14 Digitale Bildverarbeitung)

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt


def make_scale(image):
    """ Skalieren der Zahlenwerte eines Arrays, sodass gesamter
        Grauwertebereich von 0...255 umfasst wird.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # niedrigster Wert soll sein: 0 ≙ schwarz
    if np.min(image) != 0:
        image -= np.min(image)
    # hoechster Wert soll sein: 255 ≙ weiß
    weiß = 255
    hoechster_grauwert = np.max(image)
    # Berechnung Skalierungsfaktor, sodass hoechster Grauwert erfasst wird
    skal = weiß / hoechster_grauwert
    # Skalierungsfaktor auf gesamtes Szintigramm anwenden
    image *= skal
    return image


def get_image_A(laenge_quadrant, kantenlaenge, avg_a, mittelpkt):
    """ Erzeugt Objekt A, ist Quadrat.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        kantenlaenge: Kantenlaenge des Quadrats (Flaechenquelle A) in mm.

        avg_a: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt A, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).
    """
    # erstelle Array, in dem sich Flaechenquelle A befindet
    # ≙ lokales Koordinatensystem
    image_a = np.zeros((laenge_quadrant, laenge_quadrant))
    # richtige Positionierung von Flaechenquelle A im Bezug zum Rand:
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_a = image_a[abstand_y:abstand_y + kantenlaenge,
                       abstand_x:abstand_x + kantenlaenge]
    # auf jeden Pixel von Quelle A Poisson- Statistik anwenden
    # dadurch Beachtung des statistischen Charakters des
    # radioaktiven Zerfalls
    for i in range(kantenlaenge):
        for j in range(kantenlaenge):
            quelle_a[i, j] = np.random.poisson(avg_a)
    return image_a


def get_image_B(laenge_quadrant, kantenlaenge, avg_b_g, avg_b_w,
                mittelpkt, deltax):
    """ Erzeugt Objekt B, ist Quadrat mit Streifen.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        kantenlaenge: Kantenlaenge des Quadrats (Flaechenquelle B) in mm.

        avg_b_g: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, graue Streifen, in 1/mm².

        avg_b_w: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, weiße Streifen, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).

        deltax: Breite der Streifen bzw. der einzelnen Flaechenquellenpaare
        in mm.
    """
    # erstelle Array, in dem sich Flaechenquelle B befindet
    image_b = np.zeros((laenge_quadrant, laenge_quadrant))
    # TODO: Erstellung dieses Quadrats doppelt sich, schlimm?
    # richtige Positionierung von Flaechenquelle B im Bezug zum Rand:
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = laenge_quadrant + mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_b = image_b[abstand_y:abstand_y + kantenlaenge,
                       abstand_x:abstand_x + kantenlaenge]
    # Belegung der Flaeche mit zehn Paar Flaechenquellen (in Form von Streifen)
    # dafuer Anwendung Poisson- Statistik zur Charakterisierung der Streifen
    i = 0
    while i < kantenlaenge:
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_g,
                                                    (kantenlaenge, deltax))
        i += deltax
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_w,
                                                    (kantenlaenge, deltax))
        i += deltax
    return image_b


def get_image_C(laenge_quadrant, radius, avg_c, mittelpkt):
    """ Erzeugt Objekt C, ist Kreis.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        radius: Radius des Kreises in mm.

        avg_c: mittlere flaechenbezogene Zahl der registrierten Ereignisse
        von Objekt C, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).
    """
    # erstelle Array, in dem sich Flaechenquelle C befindet
    image_c = np.zeros((laenge_quadrant, laenge_quadrant))
    # lokaler Mittelpunkt (als (x, y)), von diesem aus Kreis mit Radius 50 mm
    # TODO: Berechnung Mittelpunkt lokal stimmt nur in diesem ganz speziellen
    # Fall? (ist nicht der Sinn von Parametern in Funktionen?)
    mitte_lokal = (laenge_quadrant + mittelpkt[0], -mittelpkt[1])
    # Kreisformel mit Satz des Pythagoras
    # jeden Pixel einzeln durchgehen
    for x in range(laenge_quadrant):
        for y in range(laenge_quadrant):
            deltax = mitte_lokal[0] - x
            deltay = mitte_lokal[1] - y
            if deltax**2 + deltay**2 <= radius**2:
                # Anwendung Poisson- Statistik fuer Beruecksichtigung
                # radioaktiver Zerfall
                image_c[y, x] = np.random.poisson(avg_c)
    return image_c


def get_image_D(laenge_quadrant, hoehe, avg_d, spitze):
    """ Erzeugt Objekt D, ist gleichseitiges Dreieck.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        hoehe: Hoehe des Dreiecks in mm.

        avg_d: mittlere flaechenbezogene Zahl der registrierten Ereignisse
        von Objekt D, in 1/mm².

        spitze: Koordinaten der Dreiecksspitze (x, y) in (mm, mm) im
        globalen Koordinatensystem.
    """
    # erstelle Array, in dem sich Flaechenquelle D befindet
    image_d = np.zeros((laenge_quadrant, laenge_quadrant))
    # Koordinaten der Spitze im lokalen Koordinatensystem:
    # TODO: Berechnung lokale Spitze stimmt nur in diesem ganz speziellen
    # Fall? (ist nicht der Sinn von Parametern in Funktionen?)
    spitze_lokal = (spitze[0], -spitze[1])
    # jeden Pixel der moeglichen Dreiecksflaeche einzeln durchgehen:
    # dabei wird y-Bereich von lokalen Spitze bis ... abgerastert:
    delta_y = spitze_lokal[1] + hoehe
    # jeden Pixel einzeln durchgehen
    for y in range(spitze_lokal[1], delta_y + 1):
        # aktuelle Hoehe
        akt_hoehe = np.absolute(spitze_lokal[1] - y)
        for x in range(laenge_quadrant):
            # Abstand zur Mitte ≙ aktueller x- Wert
            abstand_mitte = np.absolute(spitze_lokal[0] - x)
            # Formel zur Berechnung der Kantenlaenge des gleichseitigen
            # Dreiecks:
            # (falls Bedingung erfüllt ist, gehört Pixel zum Dreick
            # und es wird Poissonstatistik angewendet)
            if abstand_mitte <= akt_hoehe / np.sqrt(3):
                image_d[y, x] = np.random.poisson(avg_d)
    return image_d


def extract(image, y_begin, y_end, x_begin, x_end):
    """ Einteilung des Szintigramms in Quadranten und Extraktion.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        y_begin: Startpixel (in y-Richtung), welcher den Beginn des
        entsprechenden Quadranten bezeichnet. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        y_end: Pixel (in y-Richtung), welcher das Ende des
        entsprechenden Quadranten festlegt. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        x_begin: Startpixel (in x-Richtung), welcher den Beginn des
        entsprechenden Quadranten bezeichnet. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        x_end: Pixel (in x-Richtung), welcher das Ende des
        entsprechenden Quadranten festlegt. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        Zeichnung: TODO: ok?

                image:
                +-------------+--------------+
                |             |              |
                |             |              |
                |             |              |
                |             |              |
                |x_begin      |x_end         |
        y_begin +----------------------------+         +-------------+
                |             |              |         |             |
                |             |              |         |             |
                |       +-------------------------->   |             |
                |             |              |         |             |
                |             |              |         |             |
          y_end +-------------+--------------+         +-------------+

    """
    quadrant = image[y_begin:y_end, x_begin:x_end]
    return quadrant


def make_szinti():
    """ Erzeugung des Szintigramms aus Aufgabe 1.1. """
    # fuer Pixelgroeße von 256x256
    pixel = 256
    # Anzahl an Pixeln der Teilbilder (Flaechenquelle A, B, C und D, fuer
    # Erstellen (lokaler) Koordinatensysteme)
    # ≙ Mitte des globalen Koordinatensystems TODO: nicht immer?
    pixel_quadrant = pixel // 2
    # Erstellung Szintigramm = 256x256- Array
    # (Szintigramm-Flaeche ≙ globales Koordinatensystem)
    szinti = np.zeros((pixel, pixel))
    # Einteilung des Szintigramms in vier Quadranten
    # jedes Objekt befindet sich in jeweils einem Quadranten
    quadrant_eins = extract(szinti, 0, pixel_quadrant, pixel_quadrant, pixel)
    quadrant_zwei = extract(szinti, 0, pixel_quadrant, 0, pixel_quadrant)
    quadrant_drei = extract(szinti, pixel_quadrant, pixel, 0, pixel_quadrant)
    quadrant_vier = extract(szinti, pixel_quadrant, pixel,
                            pixel_quadrant, pixel)
    # Objekte dem richtigen Platz im Szintigramm zuweisen
    # (Parameter der einzelnen Flaechenquellen siehe Vorlesung zu Modul
    # MF-MRS_14 Digitale Bildverarbeitung Folie 17)
    image_a = get_image_A(pixel_quadrant, 100, 200, (60, 60))
    quadrant_eins[:, :] = image_a
    image_b = get_image_B(pixel_quadrant, 100, 250, 300, (-60, 60), 5)
    quadrant_zwei[:, :] = image_b
    image_c = get_image_C(pixel_quadrant, 50, 50, (-60, -60))
    quadrant_drei[:, :] = image_c
    image_d = get_image_D(pixel_quadrant, 100, 100, (60, -10))
    quadrant_vier[:, :] = image_d
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    szinti = make_scale(szinti)
    return szinti, pixel, pixel_quadrant


def main():
    szinti, pixel, pixel_quadrant = make_szinti()
    # Szintigramm als Plot zeichnen
    plt.figure()
    plt.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()
