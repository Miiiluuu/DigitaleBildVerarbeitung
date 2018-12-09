"""
    Aufgabe 2.9:
    Anwendung eines Bandpassfilters mit einem erlaubten Frequenzbereich von
    3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_7

# TODO: Plotfkt: (mit norm, extent usw...)


def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc. """
    fig = plt.figure(figsize=(9, 10))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(121)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 1.1])
    return ax1, ax2


def bandpassfilter(image):
    """ Erstellt Bandpassfilter mit einem bestimmten erlaubten Frequenzbereich.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        radius: definiert obere Grenzfrequenz des Tiefpassfilters, ≙ Radius
        eines Kreises, welcher tiefe Frequenzen durchlässt.
    """
    filter_kreis1 = np.zeros_like(image)
    filter_kreis2 = np.zeros_like(image)
    # Mittelpunkt des Bildes berechnen
    mitte_image = len(image) // 2           # = 128
    # Teilkreis / -filter 1:
    # Radius des Teilkreises 1 berechnen
    radius = 128 * (5 / 8)
    for x in range(len(image)):
        for y in range(len(image)):
            deltax = mitte_image - x
            deltay = mitte_image - y
            if deltax**2 + deltay**2 <= radius**2:
                filter_kreis1[y, x] = 1
    # Teilkreis / -filter 2:
    # Radius des Teilkreises 2 berechnen
    radius = 128 * (3 / 8)
    for x in range(len(image)):
        for y in range(len(image)):
            deltax = mitte_image - x
            deltay = mitte_image - y
            if deltax**2 + deltay**2 <= radius**2:
                filter_kreis2[y, x] = 1
    # Teilfilter 1 und 2 zusammensetzen zu Gesamtfilter (siehe Vorlesung zu
    # Modul MF-MRS_14 Digitale Bildverarbeitung, Folie 107)
    filter_band = filter_kreis1 - filter_kreis2
    return filter_band


def anwendung_filter_image(fourier_image, filter_image):
    """ Anwendung des Filters auf ein Bild.

        Parameter:
        ----------
        fourier_image: Fouriertransformierte des Eingabebildes, auf dem ein
        Filter angewendet wird.

        filter_image: Filter, der auf ein Eingabebild angewendet wird.
    """
    # TODO: in diese Fkt Weg vom Originalbild zum gefilterten Bild
    # (Einbeziehung Fouriertransformation)
    fourier_gefiltert = fourier_image * filter_image
    # Bild zurueckshiften
    fourier_gefiltert = np.fft.ifftshift(fourier_gefiltert)
    # Ruecktransformation Frequenz- in Ortsraum
    image_gefiltert = np.fft.ifft2(fourier_gefiltert)
    # Realteil vom Bild extrahieren
    # TODO: (Imaginärteil ist nahe Null: ergibt sich aus Rundungsfehler?)
    image_gefiltert = np.real(image_gefiltert)
    return image_gefiltert


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation: Leistungsspektrum
    fourier_szinti, _, _, _ = Aufgabe_2_7.calculate_fourier(szinti)
    # Erzeugung Bandpassfilter in Groeße des Originalbildes
    filter_band = bandpassfilter(szinti)
    # Anwendung des Tiefpassfilters auf Originalbild
    szinti_gefiltert = anwendung_filter_image(fourier_szinti, filter_band)
    # Plots
    ax1, ax2 = plot_vorbereitung('Bandpassfilterung \n'
                                 '(erlaubter Frequenzbereich: ' +
                                 '3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist)',
                                 'Originalbild', 'gefiltertes Bild')

    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])


if __name__ == "__main__":
    main()

# Interpretation:
    # mittleren Frequenzen passieren Filter, sind noch in Originalbild
    # vorhanden,übrigen Frequenzen (hohe und tiefe) werden gesperrt
    # Kanten (durch hohe Frequenzen) nur noch geringfügig drin, es lassen
    # sich nur noch Tendenzen erkennen
    # ist frequenzselektiver Filter (laesst einzelne Teile des Frequenzbandes
    # durch und sperrt andere )