"""
    Aufgabe 3.6:
    Separierung der Flaechenquelle D im Bild aus Aufgabe 1.1 (mittels
    Schwellwertverfahren).

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_3


def use_schwellwert(image, schwelle_unten, schwelle_oben):
    """ Funktion segmentiert mittels Schwellwertverfahren und a priori
        Kenntnisse einen bestimmten Bereich.
        Es wird eine Maske erstellt, diese enthaelt:
        Nullen: dieser Pixel wird als Nichtobjekt klassifiziert.
        Andere Grauwerte: dieser Pixel wird als Objekt klassifiziert.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schwelle_unten: unterer Schwellwert. Ab dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.

        schwelle_oben: oberer Schwellwert. Bis zu dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """
    # Anlegen eines Null-Arrays, welches Maske enthaelt:
    image_maske = np.zeros_like(image)
    # Schwellwertbedingung: innerhalb dieses Intervalls werden entsprechende
    # Pixel als Objekt gezaehlt und in die Maske uebernommen
    intervall_schwellen = (image >= schwelle_unten) * (image <= schwelle_oben)
    image_maske[intervall_schwellen] = image[intervall_schwellen]
    return image_maske


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # vor Anwendung Schwellwertverfahren (a priori) Glaettung mit
    # Medianfilter zur Erzeugung zusammenhaengender Gebiete, sodass Loecher in
    # Flächen teilweise aufgefuellt
    szinti_bearbeitet = Aufgabe_3_3.use_filter3x3_image(szinti)
    # aus der a priori Kenntnis von Flaechenquelle D (Parameter siehe
    # Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Aufgabe 1.1
    # (Folie 17)) werden aus (geglaetteten) Grauwerthistogramm Schwellwerte
    # visuell entnommen (sodass Gesamt-segmentierungsfehler möglichst gering)
    # und so Schwellwertgrenzen festgelegt
    szinti_bearbeitet = use_schwellwert(szinti_bearbeitet, 50, 100)
    # Darstellung der separierten Flaechenquelle D (Dreieck)
    plt.figure()
    plt.imshow(szinti_bearbeitet, cmap='gray', extent=[-128, 128, -128, 128],
               vmax=255)
    plt.show()


if __name__ == "__main__":
    main()
