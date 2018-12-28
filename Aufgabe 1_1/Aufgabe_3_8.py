"""
    Aufgabe 3.8:
    Berechnung des geometrischen und den Massenschwerpunkt fuer ein Objekt,
    bestehend aus den Flaechenquellen B und C aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_7


def calc_schwerpkt_1d(image):
    """ Funktion berechnet bestimmte Momente von Bildern und darauf aufbauend
        (in einer Dimension) den Schwerpunkt dieses Bildes entsprechend
        Vorlesung zum Modul MF-MRS_14 Digitale Bildverarbeitung, Folie 213f.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    moment0 = np.sum(image)
    x_koord = np.arange(np.shape(image)[1])
    moment = np.sum(image, axis=0) * x_koord
    moment = np.sum(moment)
    # Schwerpunkt in 1D
    schwerpkt = moment / moment0
    return schwerpkt


def calc_schwerpkt(image, calc_geometric=False):
    """ Funktion berechnet den Schwerpunkt eines Bildes (in x- und y-Richtung)
        entsprechend Vorlesung zum Modul MF-MRS_14 Digitale Bildverarbeitung,
        Folie 213f.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        calc_geometric: Falls dieser Parameter angegeben wird, wird anstatt des
        geometrischen der Massenschwerpunktes ermittelt.
    """
    # falls Berechnung vom geometrischen Schwerpunkt:
    if calc_geometric:
        # dafuer wird zuvor zunaechst logisches Bild erzeugt:
        # Bildfunktion wird auf Eins gesetzt
        image = Aufgabe_3_7.make_logic_image(image, 0)
    # Berechnung vom Schwerpunkt in x-Richtung
    schwerpkt_x = calc_schwerpkt_1d(image)
    # Berechnung vom Schwerpunkt in y-Richtung
    image_t = np.transpose(image)
    schwerpkt_y = calc_schwerpkt_1d(image_t)
    return schwerpkt_x, schwerpkt_y


def plot_schnittpkt(ueberschrift, image, schnittpkt):
    """ Funktion erstellt einen Plot mit Ueberschriften, Achsenbeschriftungen
        und Ähnliches. Es wird ein Bild geplottet mit einem Schnittpunkt
        bestimmter Geraden.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schnittpkt: enthält Koordinaten (in x- und y-Richtung), die einen
        Schnittpunkt im geplotten Bild darstellen.
    """
    plt.figure(figsize=(10, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray')
    # x-Koordinate als Vertikale plotten
    plt.axvline(schnittpkt[0], color="deeppink")
    # y-Koordinate als Horizontale plotten
    plt.axhline(schnittpkt[1], color="deeppink")
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.85])
    plt.show()


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion von Flaechenquelle B und C
    szinti = Aufgabe_1_1.extract(szinti, 0, pixel, 0, pixel_quadrant)
    # Berechnung vom geometrischen Schwerpunkt (in x- und y-Richtung)
    schwerpkt_geo = calc_schwerpkt(szinti, calc_geometric=True)
    # Einzeichnen des geometrischen Schwerpunktes
    plot_schnittpkt("geometrischer Schwerpunkt \n"
                "- innerhalb Bild aus Aufgabe 1.1 -", szinti, schwerpkt_geo)
    # Berechnung vom Massenschwerpunkt (in x- und y-Richtung)
    schwerpkt_mass = calc_schwerpkt(szinti)
    # Einzeichnen des Massenschwerpunktes
    plot_schnittpkt("Massenschwerpunkt \n"
                "- innerhalb Bild aus Aufgabe 1.1 -", szinti, schwerpkt_mass)


if __name__ == "__main__":
    main()
