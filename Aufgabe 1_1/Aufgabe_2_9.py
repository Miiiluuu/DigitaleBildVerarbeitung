"""
    Aufgabe 2.9:
    Anwendung eines Tiefpassfilters mit einer oberen Grenzfrequenz von
    |ν_lim| = 0.25 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.
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


def tiefpassfilter(image):
    """ Erstellt Tiefpassfilter mit einer oberen Grenzfreuenz: hat Form eines
        Kreises mit einem bestimmten Radius.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        radius: definiert obere Grenzfrequenz des Tiefpassfilters, ≙ Radius
        eines Kreises, welcher tiefe Frequenzen durchlässt.
    """
    filter_tief = np.zeros_like(image)
    # Mittelpunkt des Bildes berechnen
    mitte_image = len(image) // 2           # = 128
    # Radius des Kreises berechnen
    radius = 128 * 0.25
    for x in range(len(image)):
        for y in range(len(image)):
            deltax = mitte_image - x
            deltay = mitte_image - y
            if deltax**2 + deltay**2 <= radius**2:
                filter_tief[y, x] = 1
    return filter_tief


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
    # TODO: (Imaginärteil ist nahe Null: Rundungsfehler?)
    image_gefiltert = np.real(image_gefiltert)
    return image_gefiltert


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation: Leistungsspektrum
    fourier_szinti, _, _, _ = Aufgabe_2_7.calculate_fourier(szinti)
    # Erzeugung Tiefpassfilter in Groeße des Originalbildes
    filter_tief = tiefpassfilter(szinti)
    # Anwendung des Tiefpassfilters auf Originalbild
    szinti_gefiltert = anwendung_filter_image(fourier_szinti, filter_tief)
    # Plots
    ax1, ax2 = plot_vorbereitung('Tiefpassfilterung \n'
                                 '(obere Grenzfrequenz: ' +
                                 '|ν_lim| = 0.25 ∙ ν_Nvquist)', 'Originalbild',
                                 'gefiltertes Bild')
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])


if __name__ == "__main__":
    main()

# Interpretation:
    # Schaerfe ist weggenommen vom Originalbild, da hohe Frequenzen
    # rausgeschnitten wurden (hohe Frequenzen sind fuer Kanten, Abbildung
    # Details zustaendig)
    # periodisches Muster in Funktion reingebracht durch Anwenden einer
    # Kastenfunktion mit Kreis im Frequenzraum, die im Ortsraum wiederum
    # eine periodische sinc-Funktion ergibt?
