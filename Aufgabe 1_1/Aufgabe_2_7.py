"""
    Aufgabe 2.7:
    Berechnet 2D Fouriertransformierte und das Leistungsspektrum des Bildes
    aus Aufgabe 1.1

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import Aufgabe_1_1


def calculate_fourier(image):
    """ Ermittelt die 2D-dimensionale (diskrete) Fouriertransformierte sowie
        weitere Parameter (z.B. Leistungsspektrum, Amplituden- und Phasenbild
        etc., entsprechend der Vorlesung, Folie 78 aus dem Modul MF-MRS_14
        Digitale Bildverarbeitung).

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # 2D-Fouriertransformation
    fourier_image = np.fft.fft2(image)
    fourier_image = np.fft.fftshift(fourier_image)
    # Berechnung Imaginär- und Realteil der Fouriertransformierten
    imag = np.imag(fourier_image)
    real = np.real(fourier_image)
    # Ermittlung des Phasenbildes
    phase = np.arctan(imag / real)
    # Ermittlung des Leistungsspektrums
    power = real**2 + imag**2
    # Ermittlung des Amplitudenbildes
    amplitude = np.sqrt(power)
    return fourier_image, power, amplitude, phase


# TODO: plot_vorbereitungen 2, 3, 6 oder 9 Subplots in einer Fkt?
def plot_vorbereitung_3sp(ueberschrift, unterueberschrift1, unterueberschrift2,
                          unterueberschrift3, abszisse, ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        drei Subplots, Ueberschriften, Achsenbeschriftungen etc.
    """
    # Erstellen von (drei) Subplots:
    fig, axs = plt.subplots(1, 3, figsize=(10, 8), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    axs = axs.ravel()
    # TODO: Schleife??
    # Unterueberschriften der Subplots
    axs[0].set_title(unterueberschrift1)
    axs[1].set_title(unterueberschrift2)
    axs[2].set_title(unterueberschrift3)
    # Ueberlappungen vermeiden
    plt.tight_layout(w_pad=3.5, rect=[0, 0, 1, 1.4])
    # Achsenbeschriftungen und Grid
    ticks = np.linspace(-0.5, 0.5, 11)
    for i in range(3):
        axs[i].set_xlabel(abszisse)
        axs[i].set_ylabel(ordinate)
        axs[i].set_xticks(ticks)
        axs[i].set_yticks(ticks)
        axs[i].set_xticklabels(ticks, rotation=75)
    return axs


def plot_fourier(power, amplitude, phase, herkunft):
    """"Darstellung des Leistungsspektrums, Phasen- und Amplitudenbild einer
        2D-Fouriertransformierten.

        Parameter:
        ----------
        herkunft: bezeichnet jenes Bild, welches zur Erstellung des Plottes
        genutzt wird.

        power: Leistungsspektrum einer 2D-Fouriertransformierten.

        amplitude: Amplitudenspektrum einer 2D-Fouriertransformierten.

        phase: Phasenbild einer 2D-Fouriertransformierten.
    """
    axs = plot_vorbereitung_3sp(f'''Fouriertransformation {herkunft}''',
                                'Leistungsspektrum',
                                'Amplitudenbild', 'Phasenbild',
                                '$ν_{x}/ν_{Sx}$', '$ν_{y}/ν_{Sy}$')
    # Leistungsspektrum
    axs[0].imshow(power, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    # Amplitudenbild
    axs[1].imshow(amplitude, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    # Phasenbild
    axs[2].imshow(phase, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    plt.show()


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation
    fourier_image, power, amplitude, phase = calculate_fourier(szinti)
    # graphische Darstellung der Fouriertransformierten
    plot_fourier(power, amplitude, phase, "des Bildes aus Aufgabe 1.1")


if __name__ == "__main__":
    main()

# Interpretation:
    # Phasenbild codiert raeumliche Info
    # Linien entsprechen Aenderungen in Grauwerten / Farbspruenge / Kanten
    # gar keine Linien hier? keine Farbaenderungen?
