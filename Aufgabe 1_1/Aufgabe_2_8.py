"""
    Aufgabe 2.8:
    Dreht das Bild aus Aufgabe 1.1 um 30° im positiven Drehsinne, berechnet
    die Fouriertransformierte und vergleicht das Ergebnis mit dem aus Aufgabe
    2.7.
    
    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_2_7


def drehmatrix(grad):
    """ Drehung eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        grad: Angabe der Drehung in Grad (im positivem Drehsinne) in Grad.
    """
    # Umrechnung Winkel in Bogenmaß
    grad_rad = np.radians(grad)
    # Drehmatrix in homogenen Koordinaten
    dreh = np.array([[np.cos(grad_rad), np.sin(grad_rad), 0],
                     [-np.sin(grad_rad), np.cos(grad_rad), 0], [0, 0, 1]])
    # Drehmatrix invertieren, da Transformation im positiven Sinn
    dreh = np.linalg.inv(dreh)
    return dreh


# TODO: Grauwertappromimation!
def transformation(image, pixel_mitte, transform):
    """ Transformation eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.
        TODO: nicht immer perfekt eingehalten?
        
        transform: Transformationsmatrix, die Transformation eines Bildes
        durchfuehrt.
    """
    image_transform = np.zeros_like(image)
    # Schleife:
    # jeden Pixel einzeln durchgehen, auf diesem Drehmatrix anwenden
    # und neue rotierte Koordinaten berechnen
    # Rotation mit Drehmatrix bezieht sich auf Nullpunkt des Koordinatensystems
    # das heißt fuer eine Drehung um die Mitte des Bildes muss der Nullpunkt
    # des Koordinatensystems in die Mitte des Bildes gelegt werden
    # (ansonsten Drehung um obere linke Ecke des Bildes)
    for x in range(-pixel_mitte, pixel_mitte):
        for y in range(-pixel_mitte, pixel_mitte):
            # Rotationsmatrix auf alle x-Werte anwenden
            koord_xy_transform = (transform @ np.array([x, y, 1]))
            x_transform = np.int_(np.round(koord_xy_transform[0]))
            y_transform = np.int_(np.round(koord_xy_transform[1]))
            # Pixel des Null-Arrays (image_transform) auffuellen:
            # Pruefen, ob rotierter Wert innerhalb Bereich Originalbild
            # vorkommt
            # wenn Bedingung erfuellt existieren Grauwerte im Originalbild,
            # die ins rotierte Bild an der richtigen Stelle uebernommen werden
            # (ansonsten Nullen an dieser Stelle)
            if (-pixel_mitte <= x_transform < pixel_mitte) and \
               (-pixel_mitte <= y_transform < pixel_mitte):
                # Addieren vom Zahlenwert des Pixels,von Mitte des 
                # Koordinatensystems, um Array nicht mit negativen Indices
                # anzusprechen (wuerde falsche Werte liefern)
                image_transform[y + pixel_mitte, x + pixel_mitte] = \
                    image[y_transform + pixel_mitte, x_transform + pixel_mitte]
    return image_transform

    
def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Plots fuer Ortsraum Originalbild und gedrehtes Bild erstellen:
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp('Ortsraum',
                                                 'Originalbild aus ' +
                                                 'Aufgabe 1.1', 
                                                 'um 30° gedrehtes Bild')
    # Plot Originalbild Ortsraum
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Drehmatrix erstellen (um 30° im positivem Sinne)
    dreh = drehmatrix(30)
    # Erstellung gedrehtes Originalbild Ortsraum
    szinti_transform = transformation(szinti, pixel_quadrant, dreh)
    # Plot gedrehtes Originalbild Ortsraum
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])
    
    # Plots fuer Frequenzraum Originalbild und gedrehtes Bild erstellen:
    ax3, ax4 = Aufgabe_2_1.plot_vorbereitung_2sp('Frequenzraum - ' +
                                                'Leistungsspektrum',
                                                'Originalbild aus Aufgabe 1.1',
                                                'um 30° gedrehtes Bild',
                                                '$ν_{x}/ν_{Sx}$',
                                                '$ν_{y}/ν_{Sy}$', ticks=True)
    # Fouriertransformation: Erstellung Leistungsspektrum
    _, power, _, _ = Aufgabe_2_7.calculate_fourier(szinti)
    # Plot Leistungsspektrum
    ax3.imshow(power, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    # Erstellung gedrehtes Leistungsspektrum
    power_transform = transformation(power, pixel_quadrant, dreh)
    # Plot Leistungsspektrum gedrehtes Bild
    ax4.imshow(power_transform, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.show()
    

if __name__ == "__main__":
    main()

# Interpretation:
  # eine Drehung der Ortsfunktion um den Winkel alpha fuehrt zu einer
  # gleichartigen Drehung der entsprechenden Frequenzfunktion im Frequenzraum
