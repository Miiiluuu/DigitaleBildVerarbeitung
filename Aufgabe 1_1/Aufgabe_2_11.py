"""
    Aufgabe 2.11:
    Anwendung eines Hochpassfilters mit einem erlaubten Frequenzbereich von
    3/4 ∙ ν_Nvquist < |ν| < ν_Nvquist auf das Bild aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_2_9


def make_hochpassfilter(image, anteil, pixel_mitte):
    """ Erstellt Hochpassfilter (in Groeße eines Bildes 'image',
        Filterform Kreis), welcher nur hohe Frequenzen durchlaesst.
    """
    # Erstellung Kreisfilter
    filter_kreis = Aufgabe_2_9.make_kreisfilter(image, anteil, pixel_mitte)
    # inverser Kreis- ist Hochpassfilter
    filter_hochpass = 1 - filter_kreis
    return filter_hochpass


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erzeugung Tiefpassfilter (in Groeße des Originalbildes)
    filter_hochpass = make_hochpassfilter(szinti, (3 / 4), pixel_quadrant)
    # Anwendung des Tiefpassfilters auf Originalbild
    szinti_gefiltert = Aufgabe_2_9.use_filter(szinti, filter_hochpass)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp('Hochpassfilterung \n'
                                        '(erlaubter Frequenzbereich: ' +
                                        '3/4 ∙ ν_Nvquist < |ν| < ν_Nvquist',
                                        'Originalbild', 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()

# Interpretation:
    # hohe Frequenzen des Originalbildes noch vorhanden
    # (sind fuer Kanten, Abbildung Details zustaendig)
    # d.h. strukturreiche/detailreiche Elemente gut zu sehen
    # aber dafuer sind niedrige Frequenzen, welche homogene Bereiche des
    # Bildes, kontinuierliche (Grauwert)uebergaenge darstellen, weg

