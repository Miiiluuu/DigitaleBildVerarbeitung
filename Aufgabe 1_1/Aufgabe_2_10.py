"""
    Aufgabe 2.10:
    Anwendung eines Bandpassfilters mit einem erlaubten Frequenzbereich von
    3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_2_9


def bandpassfilter(image, anteil_up, anteil_down, pixel_mitte):
    """ Erstellt Bandpassfilter mit einem bestimmten erlaubten Frequenzbereich.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        anteil_up: Anteil der Nyquistfrequenz, welche obere Grenzfrequenz des
        Bandpassfilters bestimmt.

        anteil_down: Anteil der Nyquistfrequenz, welche untere Grenzfrequenz
        des Bandpassfilters bestimmt.

        pixel_mitte: Pixel, bei dem hier Mitte des Koordinaensystems liegt.
    """
    # Teilkreis / -filter 1:
    filter_kreis1 = Aufgabe_2_9.make_kreisfilter(image, anteil_up, pixel_mitte)
    # Teilkreis / -filter 2:
    filter_kreis2 = Aufgabe_2_9.make_kreisfilter(image, anteil_down,
                                                 pixel_mitte)
    # Teilfilter 1 und 2 zusammensetzen zu Gesamtfilter (entspricht
    # Bandpassfilter, siehe Vorlesung zu Modul MF-MRS_14 Digitale
    # Bildverarbeitung, Folie 107)
    filter_band = filter_kreis1 - filter_kreis2
    return filter_band


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erzeugung Bandpassfilter (in Groeße des Originalbildes)
    filter_band = bandpassfilter(szinti, (5 / 8),  (3 / 8), pixel_quadrant)
    # Anwendung des Bandpassfilters auf Originalbild
    szinti_gefiltert = Aufgabe_2_9.use_filter(szinti, filter_band)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp('Bandpassfilterung \n'
                                '(erlaubter Frequenzbereich: ' +
                                '3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist)',
                                'Originalbild', 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()

# Interpretation!!!
    # mittleren Frequenzen passieren Filter, sind noch in Originalbild
    # vorhanden,übrigen Frequenzen (hohe und tiefe) werden gesperrt
    # Kanten (durch hohe Frequenzen) nur noch geringfügig drin, es lassen
    # sich nur noch Tendenzen erkennen
    # ist frequenzselektiver Filter (laesst einzelne Teile des Frequenzbandes
    # durch und sperrt andere )