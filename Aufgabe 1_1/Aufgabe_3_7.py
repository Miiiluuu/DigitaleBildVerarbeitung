"""
    Aufgabe 3.6:
    Extrahieren des rechten unteren Quadranten des Bild aus Aufgabe 1.1
    (Flaechenquelle D, gleichseitiges Dreieck) als Teilbild. Dabei Durchführung
    einer Kantenextraktiion mit anschließender Hough-Transformation.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_4
# TODO: doppelte Plot-Funktion? Figuresize




def berechnung_flaeche_dreieck(hoehe):
    """ Berechnung der Flaeche eines Dreieckes 'objekt' in Pixeln.

        Parameter:
        ----------
        hoehe: Hoehe des gleicheitigen Dreiecks in mm.
    """
    # Berechnung der Seitenlaenge a eines gleichseitigen Dreiecks aus der Hoehe
    a = 2 * hoehe / np.sqrt(3)
    # Berechnung des Flaecheninhaltes eines gleichseitigen Dreiecks aus der
    # Seitenlaenge a
    flaeche = np.sqrt(3) * a**2 / 4     # Einheit: in mm² bzw Anzahl Pixel, da
                                        # 1 Pixel 1 mm² entspricht
    return flaeche


def separiere_objekt(image, flaeche):
    """ Funktion sucht in einem Bild 'image', ob dessen Haufigkeitsverteilung
        einen Bereich desselben Grauwertes besitzt, wobei dieser Bereich einem
        bestimmten Flaecheninhalt entspricht und separiert dieses Objekt. 

        Parameter:
        ----------
        image: Array, Eingabewerte.
        
        flaeche: Flaecheninhalt in Anzahl an Pixeln eines bestimmten Objektes.
    """
    # Berechnung der Haeufigkeitsverteilung
    ordinate, _, _ = plt.hist(image.flatten(), bins=256, density=True)
    # Bereich finden, der denselben Grauwert  bzw lamda 100 von
    # Poissonverteilung besitzt und gleichzeitig bestimmter Flaeche in Anzahl
    # Pixeln eines gleichseitigen Dreieck entspricht
    # TODO: Derselbe Grauwert, ohne dessen Kenntniss vorauszusetzen?
    if (... lambda richtig mit Abweichung < np.exp(-17)) and
        np.sum(DIESER ordinaten-Werte) = flaeche (mit geringem Fehler):
            # Wenn Bedingung zutrifft, wird dieser Ordinatenwert beibehalten,
            # alle anderen Ordinatenwerte werden auf Null gesetzt
            # Umkehrfunktion von hist, um Bild wieder darzustellen
            # aus Histgramm?
    return objekt_separiert
   
    
def plot(ueberschrift, image):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.

        Parameter:
        ----------
        image: Array, Eingabewerte, welche im Plot dargestellt werden.
    """
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray', extent=[-128, 128, -128, 128])


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Anwendung Sobelfilter aufs Bild aus Aufgabe 1.1 zur Kantenextraktion
    # (und Glaettung)
    szinti_sobel_ges = Aufgabe_3_4.filter_sobel_image(szinti)
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des rechten unteren Quadranten
    quadrant_vier = szinti[128:256, 128:256]
    # (virtueller) Ursprung des Bildes wird in das Zentrum des Teilbildes
    # gelegt!
    # nur Pixel durchgehen, indem auch Wert > Null gespeichert ist?
    # ich kenne Seitenlaenge a
    # alle Winkel in Bereich [0, pi] durchgehen:
    for grad in range(np.pi):
        # was fuer Koordinaten erhaelt man fuer dasselbe alpha?
        # Berechnen der Koordinaten entsprechend der Hesse'schen Normalform
        # der Geradengleichung, diese Koordinaten liegen auf einer Linie
    # Anwendung Sobelfilter: logisches Binaerbild! Konturverkettung?


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?

# Interpretation:
    # Laplace: Hochpass zum Hervorheben strukturreicher Bildbereiche, da
    # diese kruemmungsempfindlich sind
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
