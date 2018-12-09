u"""
    Aufgabe 2.8:
    Dreht das Bild aus Aufgabe 1.1 um 30° im positiven Drehsinne, berechnet
    die Fouriertransformierte und vergleicht das Ergebnis mit dem aus Aufgabe
    2.7.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import Aufgabe_1_1
import Aufgabe_2_7

# TODO: doppelte Plot-Funktion? Achsenbeschriftungen

def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2,
                      abszisse='', ordinate=''):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.
    """
    fig = plt.figure(figsize=(7, 8))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(121)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 1.4])
    return ax1, ax2


def drehung(image, grad, pixel_mitte):
    """ Drehung eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).
    
        Parameter:
        ----------
        image: Array, Eingabewerte.
        
        grad: Angabe der Drehung in Grad (im positivem Drehsinne) in Grad.
        
        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.
    """
    # Anlegen Null-Array
    image_rotate = np.zeros_like(image)
    # Umrechnung Winkel in Bogenmaß
    grad_rad = np.radians(grad)
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
            x_rotate = np.int(np.round((x) * np.cos(grad_rad) +
                                    (y) * -np.sin(grad_rad)))
            # Rotationsmatrix auf alle y-Werte anwenden
            y_rotate = np.int(np.round((x) * np.sin(grad_rad) +
                                    (y) * np.cos(grad_rad)))
            # Pixel des Null-Arrays (image_rotate) auffuellen:
            # Pruefen, ob rotierter Wert innerhalb Bereich Originalbild
            # vorkommt
            # wenn Bedingung erfuellt existieren Grauwerte im Originalbild,
            # die ins rotierte Bild an der richtigen Stelle uebernommen werden
            # (ansonsten Nullen an dieser Stelle)
            if (-pixel_mitte <= x_rotate < pixel_mitte) and \
               (-pixel_mitte <= y_rotate < pixel_mitte):
                # Addieren von 128 (pixel_quadrant), um Array nicht mit
                # negativen Indices anzusprechen (wuerde falsche Werte liefern)
                image_rotate[y + pixel_mitte, x + pixel_mitte] = \
                    image[y_rotate + pixel_mitte, x_rotate + pixel_mitte]
    return image_rotate
    
    
def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation: Leistungsspektrum
    _, power, _, _ = Aufgabe_2_7.calculate_fourier(szinti)
    # Plots:
    # Ortsraum Originalbild und gedrehtes Bild
    ax1, ax2 = plot_vorbereitung('Ortsraum', 'Originalbild aus Aufgabe 1.1',
                                  'um 30° gedrehtes Bild')
    # Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # gedrehtes Bild (um 30° im positivem Sinne)
    szinti_rotate = drehung(szinti, 30, pixel_quadrant)
    ax2.imshow(szinti_rotate, cmap='gray', extent=[-128, 128, -128, 128])
    
    # Frequenzraum Originalbild und gedrehtes Bild 
    ax3, ax4 = plot_vorbereitung('Frequenzraum - Leistungsspektrum',
                                 'Originalbild aus Aufgabe 1.1',
                                 'um 30° gedrehtes Bild',
                                 '$ν_{x}/ν_{Sx}$', '$ν_{y}/ν_{Sy}$')
    # Leistungsspektrum Originalbild
    ax3.imshow(power, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    ticks = np.linspace(-0.5, 0.5, 11)
    ax3.set_xticks(ticks)
    ax3.set_yticks(ticks)
    ax3.set_xticklabels(ticks, rotation=75)
    # Leistungsspektrum gedrehtes Bild (um 30° im positivem Sinne)
    power_rotate = drehung(power, 30, pixel_quadrant)
    ax4.imshow(power_rotate, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    ax4.set_xticks(ticks)
    ax4.set_yticks(ticks)
    ax4.set_xticklabels(ticks, rotation=75)

    
if __name__ == "__main__":
    main()

# Interpretation:
  # eine Drehung der Ortsfunktion um den Winkel alpha fuehrt zu einer
  # gleichartigen Drehung der entsprechenden Frequenzfunktion im Frequenzraum
  # Drehung im Frequenzraum richtig?
