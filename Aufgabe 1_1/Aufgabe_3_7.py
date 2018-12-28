"""
    Aufgabe 3.7:
    Extrahieren des rechten unteren Quadranten des Bild aus Aufgabe 1.1
    (Flaechenquelle D, gleichseitiges Dreieck) als Teilbild. Dabei Durchführung
    einer Kantenextraktiion mit anschließender Hough-Transformation.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_4
import Aufgabe_3_3


def make_logic_image(image, schwelle):
    """ Funktion erzeugt aus einem Bild ein logisches Bild (Binaerbild), indem
        ein bestimmter Bereich mittels des Schwellwertverfahrens separiert
        wird. Dabei werden a priori Kenntnisse vorausgesetzt
        (Grauwerthistogramm u.Ä.).
        Beinhaltet Pixelklassifikation: Einteilung in Objekt- (enthaelt Einsen)
        und Nichtobjektpixel (enthaelt Nullen).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schwelle: Schwellwert. Ab naechstgroeßeren Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """
    image_maske = np.zeros_like(image)
    image_maske[schwelle < image] = 1
    return image_maske


def extract_values(image, value):
    """ Funktion speichert aus einem Array die einander zugehoerigen (x- und
         y-) Koordinaten (als Meshgrid), welche einen bestimmten Wert 'value'
         enthalten. Dabei wird der (virtuelle) Ursprung in das Zentrum des
         Bildes gelegt.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        value: bestimmter Wert, anhand dessen Filterung der Werte.
    """
    # Zentrum des Bildes
    center = len(image) // 2
    # Abspeichern der einander zugehoerigen Koordinaten
    koord_x, koord_y = np.meshgrid(np.arange(-center, center),
                                   np.arange(center, -center, step=-1))
    # Rausfilterung der Untergrundwerte nach einen bestimmten Wert 'value'
    koord_x = koord_x[image == value]
    koord_y = koord_y[image == value]
    return koord_x, koord_y


def plot_2d_hist(ueberschrift, abszisse, ordinate, werte1, werte2):
    """ Plot eines 2D-Histogramms mit entsprechender Ueberschrift,
        Achsenbeschriftung, Farbskala etc.
    """
    plt.figure(figsize=(10, 6))
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle(ueberschrift, fontsize=16)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # TODO: warum genau diese Werte? kann nicht vorausgesetzt werden?
    counts, xedges, yedges, image = plt.hist2d(werte1, werte2, bins=180,
                                               range=[[0, 180], [-64, 64]])
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.8])
    # TODO: Colorbarbeschriftung
    plt.colorbar(image)
    plt.show()


def szinti_vorverarbeitung(szinti, pixel, pixel_quadrant):
    """ Funktion leistet Vorverarbeitung des Bildes aus Aufgabe 1.1 fuer
        anschließende Kantenorientierte Segmentierung (Hough-Transformation).
        Kanten werden extrahiert durch Anwendung verschiedener Filter und
        Aehnliches.
    """
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des rechten unteren Quadranten
    quadrant_vier = Aufgabe_1_1.extract(szinti, pixel_quadrant, pixel,
                                        pixel_quadrant, pixel)
    # Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete, sodass
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.use_filter3x3_image(quadrant_vier)
    # Anwendung Sobelfilter aufs Teilbild (Flaechenquelle D) aus Bild
    # Aufgabe 1.1 zur Kantenextraktion
    quadrant_vier = Aufgabe_3_4.filter_sobel_image(quadrant_vier)
    # 2tes mal Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # sodass Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.use_filter3x3_image(quadrant_vier)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    quadrant_vier = Aufgabe_1_1.make_scale(quadrant_vier)
    # a priori werden Schwellwertgrenzen festgelegt, wodurch lediglich Kanten
    # extrahiert werden
    quadrant_vier_kanten = make_logic_image(quadrant_vier, 160)
    # Extrahieren (nur) der (x- und y-) Koordinaten, bei denen Bildfunktion
    # f(x) ungleich 0
    # (d.h. in neuen Koordinaten-arrays sind lediglich Koordinaten der Kanten
    # (entsprechen Einsen im logischen Bild) enthalten)
    koord_x, koord_y = extract_values(quadrant_vier_kanten, 1)
    return koord_x, koord_y


def hough_trafo(koord_x, koord_y):
    """ Anwenden der Hough-Transformation = Kantenorientierte Segmentierung.
        Mittels der Hesseschen Normalform fuer Geradengleichungen werden
        Geraden erkannt (siehe Vorlesung zu Modul MF-MRS_14 Digitale
        Bildverarbeitung, Folie 202f). Dafuer wird der Normalenvektor vom
        (virtuellen) Ursprung des Bildes und der zugehoerige Winkel
        parametrisiert.

        Parameter:
        ----------
        koord_x: (x-)Koordinaten einer Bildfunktion f(x, y), fuer die gilt:
        f(x, y) ungleich 0 .

        koord_y: (y-)Koordinaten einer Bildfunktion f(x, y), fuer die gilt:
        f(x, y) ungleich 0 .
    """
    winkel = []
    abstaende = []
    # verschiedene Winkel durchgehen
    for alpha in np.linspace(0, 180, 180, endpoint=False):
        # einzelne aktuelle Winkel abspeichern (Anzahl entsprechend Anzahl
        # der Koordinaten)
        winkel.append(np.ones(len(koord_x)) * alpha)
        # Winkel in Bogenmaß umrechen
        alpha = np.radians(alpha)
        # Hessesche Normalform der Geradengleichung: Abstaende berechnen
        abstand = koord_x * np.cos(alpha) + koord_y * np.sin(alpha)
        # zu aktuellen Winkel alle dazu berechneten Abstaende abspeichern
        abstaende.append(abstand)
    # Umwandeln der Listen in Arrays
    winkel = np.array(winkel).ravel()
    abstaende = np.array(abstaende).ravel()
    # Darstellung der verketteten Kanten / durchgezogenen Linien des Dreieckes
    # als Häufungspunkte im 2D-Histogramm
    plot_2d_hist("Kantenorientierte Segmentierung \n"
                 "- Hough-Transformation zur Erkennung der Seiten des \n"
                 "Dreieckes aus Flaechenquelle D, Aufgabe 1.1 -",
                 r'Winkel $ϕ/°$', r'Abstand zum Mittelpunkt $d/mm$', winkel,
                 abstaende)


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Vorverarbeitung des Bildes: Voraussetzung fuer Hough-Transformation
    # ist Kantenextraktion
    koord_x, koord_y = szinti_vorverarbeitung(szinti, pixel, pixel_quadrant)
    # Finden der Kantenpunkte, die zu einer (durchgehenden) Linie gehoeren
    # (und demnach kein Rauschen sind) mittels Hough-Transformation
    # (siehe Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Folie
    # 202f):
    # Finden der Kantenpunkte, die zu einer (durchgehenden) Linie gehoeren
    # (und demnach kein Rauschen sind)
    hough_trafo(koord_x, koord_y)


if __name__ == "__main__":
    main()
