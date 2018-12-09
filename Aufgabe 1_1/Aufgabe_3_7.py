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
import Aufgabe_2_2
import Aufgabe_3_3
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
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des rechten unteren Quadranten
    quadrant_vier = szinti[128:256, 128:256]
    # 1tes Mal Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.filter_image(quadrant_vier)
    # Anwendung Sobelfilter aufs Teilbild (Flaechenquelle D) aus Bild
    # Aufgabe 1.1 zur Kantenextraktion
    # (und Glaettung)
    quadrant_vier = Aufgabe_3_4.filter_sobel_image(quadrant_vier) 
    # 2tes mal Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.filter_image(quadrant_vier)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    quadrant_vier = Aufgabe_1_1.make_scale(quadrant_vier)
    # Kontrolldarstellung
    plt.figure()
    plt.imshow(quadrant_vier, cmap='gray')
    # logisches Bild (Binaerbild) aufbauen: mit Kanten Eins, Rest Null
    # dafür Histogramm anschauen
    plt.figure()
    Aufgabe_2_2.erstelle_grauwerthistogramm_abgeschnitten('Grauwerthistogramm',
                                'fuer Bild aus Aufgabe 1.1, ' +
                                'gekuerzte Ordinatenachse', r'$f$',
                                'Häufigkeitsverteilung $h(f)$',
                                quadrant_vier.flatten())
    # a priori werden Schwellwertgrenzen festgelegt, welche Grauwerte als
    # Objekt und welche als Untergrund gesetzt werden, sodass Kanten extrahiert
    # werden
    quadrant_vier_kanten = np.zeros_like(quadrant_vier)
    quadrant_vier_kanten[160 <= quadrant_vier] = 1
    plt.figure()
    plt.imshow(quadrant_vier_kanten, cmap='gray')
    # neues Array anlegen, indem lediglich Koordinaten der Kanten (entsprechen
    # Einsen im logischen Bild) enthalten sind (d.h. f(x,y) ungleich 0)
    koord_x, koord_y = np.meshgrid(np.arange(-64, 64),
                                    np.arange(-64, 64))
    # rausfiltern der Untergrundwerte: Extrahieren der Kanten!
    koord_x = koord_x[quadrant_vier_kanten == 1]
    koord_y = koord_y[quadrant_vier_kanten == 1]
    # welche Kantenpunkte gehören nun zu einer (durchgehenden) Linie?
    # Pruefen mit Hough-Transformation
    # (siehe Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Folie
    # 202f)
    # verschiedene Winkel durchgehen
    winkel = []
    abstaende = []
    for alpha in np.linspace(0, 180, 180, endpoint=False):
        # einzelne Winkel abspeichern (so viele wie abstande)
        winkel.append(np.ones(len(koord_x))*alpha)
        # Winkel in Bogenmaß umrechen
        alpha = np.radians(alpha)
        # Hessesche Normalform der Geradengleichung
        abstand = koord_x * np.cos(alpha) + koord_y * np.sin(alpha)
        # zu aktuellen Winkel alle dazu berechneten Abstaende abspeichern
        abstaende.append(abstand)
    # Umwandeln der Listen in Arrays
    winkel = np.array(winkel).ravel()
    abstaende = np.array(abstaende).ravel()
    # 2D-Histogramm aus Abstaenden und Winkel darstellen
    plt.figure()
    counts, xedges, yedges, image = plt.hist2d(winkel, abstaende, bins=100)
        
#    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
#    # Extraktion des rechten unteren Quadranten
#    quadrant_vier = szinti[128:256, 128:256]
#    # (virtueller) Ursprung des Bildes wird in das Zentrum des Teilbildes
#    # gelegt!
#    # nur Pixel durchgehen, indem auch Wert > Null gespeichert ist?
#    # ich kenne Seitenlaenge a
#    # alle Winkel in Bereich [0, pi] durchgehen:
##    for grad in range(np.pi):
##        # was fuer Koordinaten erhaelt man fuer dasselbe alpha?
##        # Berechnen der Koordinaten entsprechend der Hesse'schen Normalform
##        # der Geradengleichung, diese Koordinaten liegen auf einer Linie
##    # Anwendung Sobelfilter: logisches Binaerbild! Konturverkettung?


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?

# Interpretation:
    # Laplace: Hochpass zum Hervorheben strukturreicher Bildbereiche, da
    # diese kruemmungsempfindlich sind
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
