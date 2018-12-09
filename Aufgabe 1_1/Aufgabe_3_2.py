"""
    Aufgabe 3.2:
    Fuehrt nacheinander zunaechst eine Rotation um 90° (im positiven Drehsinne)
    und anschließend eine Scherung auf das Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
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


def transformationsmatrix(grad):
    """ Drehung eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        grad: Angabe der Drehung in Grad (im positivem Drehsinne) in Grad.

        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.
    """
    # Umrechnung Winkel in Bogenmaß
    grad_rad = np.radians(grad)
    # Drehmatrix in homogenen Koordinaten
    dreh = np.array([[np.cos(grad_rad), np.sin(grad_rad), 0],
                     [-np.sin(grad_rad), np.cos(grad_rad), 0], [0, 0, 1]])
    # Scherung in homogenen Koordinaten
    scherung = np.array([[1, -(np.sqrt(2) / 2), 0],
                         [0, (np.sqrt(2) / 2), 0], [0, 0, 1]])
    # Matrizen invertieren, da Transformation im positiven Sinn
    dreh = np.linalg.inv(dreh)
    scherung = np.linalg.inv(scherung)
    # Transformationsmatrix:
    # Hintereinander-Ausfuehrung von Drehung und Scherung durch einfaches
    # Multiplizieren der einzelnen Transformationsmatrizen
    transform = (dreh @ scherung)
    return transform


def transformation(image, pixel_mitte, transform):
    """ Drehung eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.

        transform: Transformationsmatrix, fuehrt zunaechst Drehung (um 90° im
        positiven Sinn) und anschließend Scherung durch.
    """
    # Anlegen Null-Array
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
                # Addieren von 128 (pixel_quadrant), um Array nicht mit
                # negativen Indices anzusprechen (wuerde falsche Werte liefern)
                image_transform[y + pixel_mitte, x + pixel_mitte] = \
                    image[y_transform + pixel_mitte, x_transform + pixel_mitte]
    return image_transform


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Plots:
    # Originalbild und transformiertes Bild
    ax1, ax2 = plot_vorbereitung('Ortsraum', 'Originalbild aus Aufgabe 1.1',
                                 'transformiertes Bild')
    # Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Transformationmatrix erstellen:
    # mit 30° als Winkel
    transform = transformationsmatrix(90)
   
# TODO: Drehung und Scherung in einzelne Funktionen!  (damit wiederverwendbar)
#    dreh = drehmatrix(90)
#    scher = schermatrix(np.sqrt(2)/2)
#    transform = dreh @ scher
    
    # Transformationsmatrix auf Bild aus Aufgabe 1.1 anwenden
    # (positive Drehung um 90°, Scherung)
    szinti_transform = transformation(szinti, pixel_quadrant, transform)
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])


if __name__ == "__main__":
    main()

# Interpretation:
    # eine Drehung der Funktion im Ortsraum fuehrt zu einer gleichartigen Drehung
    # im Frequenzraum
    # Drehung im Frequenzraum richtig?
