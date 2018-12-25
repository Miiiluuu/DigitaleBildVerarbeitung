"""
    Aufgabe 3.2:
    Fuehrt nacheinander zunaechst eine Rotation um 90° (im positiven Drehsinne)
    und anschließend eine Scherung auf das Bild aus Aufgabe 1.1 durch.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_2_8


def transformationsmatrix(dreh):
    """ Transformation eines Bildes:
        Diese Matrix fuehrt zunaechst eine Drehung (im positivem Drehsinne)
        und anschließend eine Scherung (entsprechend Vorlesung, Folie 136 aus
        dem Modul MF-MRS_14 Digitale Bildverarbeitung) durch.

        Parameter:
        ----------
        dreh: Drehmatrix, welche zuerst auf das Bild angewendet werden soll.
        Danach erfolgt eine Scherung.
    """
    # Schermatrix in homogenen Koordinaten
    scherung = np.array([[1, -(np.sqrt(2) / 2), 0],
                         [0, (np.sqrt(2) / 2), 0], [0, 0, 1]])
    # Schermatrix invertieren, da Transformation im positiven Sinn
    scherung = np.linalg.inv(scherung)
    # Transformationsmatrix:
    # Hintereinander-Ausfuehrung von Drehung und Scherung durch einfaches
    # Multiplizieren der einzelnen Transformationsmatrizen
    transform = (dreh @ scherung)
    return transform


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Plots:
    # Plots (fuer Originalbild und transformiertes Bild aus Aufgabe 1.1)
    # erstellen
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp('Ortsraum', 'Originalbild ' +
                                                 'aus Aufgabe 1.1',
                                                 'transformiertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Drehmatrix mit 30° als Winkel erstellen
    dreh = Aufgabe_2_8.drehmatrix(90)
    # Transformationmatrix erstellen
    transform = transformationsmatrix(dreh)
    # Transformationsmatrix auf Bild aus Aufgabe 1.1 anwenden
    # (positive Drehung um 90°, Scherung)
    szinti_transform = Aufgabe_2_8.transformation(szinti, pixel_quadrant,
                                                  transform)
    # Plot transformiertes Bild aus Aufgabe 1.1
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()

