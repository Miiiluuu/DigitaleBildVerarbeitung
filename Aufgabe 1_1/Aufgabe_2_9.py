"""
    Aufgabe 2.9:
    Anwendung eines Tiefpassfilters mit einer oberen Grenzfrequenz von
    |ν_lim| = 0.25 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_2_7


def make_kreisfilter(image, anteil, pixel_mitte):
    """ Erstellt Filter (in Groeße eines Bildes 'image', Filterform Kreis)
        mit einer oberen Grenzfrequenz: hat Form eines Kreises mit einem
        bestimmten Radius.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        anteil: Anteil der Nyquistfrequenz, welche obere Grenzfrequenz des
        Tiefpassfilters bestimmt.

        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.
        TODO: nicht immer perfekt eingehalten?
    """
    filter_kreis = np.zeros_like(image)
    # TODO: pixel_mitte (128) ≙ Nyquist-Frequenz. warum?
    # Radius eines Kreises berechnen, welcher tiefe Frequenzen durchlässt
    # (definiert obere Grenzfrequenz des Tiefpassfilters)
    radius = pixel_mitte * anteil       # TODO: pixel_mitte = 128 = ν_Nvquist?
                                        # nur in diesem Fall: Allgemein?
    for x in range(len(image)):
        for y in range(len(image)):
            deltax = pixel_mitte - x
            deltay = pixel_mitte - y
            if deltax**2 + deltay**2 <= radius**2:
                filter_kreis[y, x] = 1
    return filter_kreis


def use_filter(image, filter_image):
    """ Anwendung des Filters auf ein Bild. Dafuer wird Fouriertransformation
        des Eingabebildes berechnet. Die Fouriertransformierte wird
        anschließend gefiltert (durch eine Multiplikation der Filtermaske, im
        Frequenzraum).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_image: Filter, der auf ein Eingabebild angewendet wird.
    """
    # Fouriertransformation des Eingabebildes
    fourier_image, _, _, _ = Aufgabe_2_7.calculate_fourier(image)
    # Multiplikation im Frequenzraum
    fourier_gefiltert = fourier_image * filter_image
    # Bild zurueckshiften
    fourier_gefiltert = np.fft.ifftshift(fourier_gefiltert)
    # Ruecktransformation Frequenz- in Ortsraum
    image_gefiltert = np.fft.ifft2(fourier_gefiltert)
    # Realteil vom Bild zur spaeteren graphischen Darstellung extrahieren
    image_gefiltert = np.real(image_gefiltert)
    return image_gefiltert


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erzeugung Tiefpassfilter (in Groeße des Originalbildes)
    filter_tief = make_kreisfilter(szinti, 0.25, pixel_quadrant)
    # Anwendung des Tiefpassfilters auf Originalbild
    szinti_gefiltert = use_filter(szinti, filter_tief)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp('Tiefpassfilterung \n'
                                                 '(obere Grenzfrequenz: ' +
                                                 '|ν_lim| = 0.25 ∙ ν_Nvquist)',
                                                 'Originalbild',
                                                 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()

# Interpretation:
    # Schaerfe ist weggenommen vom Originalbild, da hohe Frequenzen
    # rausgeschnitten wurden (hohe Frequenzen sind fuer Kanten, Abbildung
    # Details zustaendig)
    # periodisches Muster in Funktion reingebracht durch Anwenden einer
    # Kastenfunktion mit Kreis im Frequenzraum, die im Ortsraum wiederum
    # eine periodische sinc-Funktion ergibt?
