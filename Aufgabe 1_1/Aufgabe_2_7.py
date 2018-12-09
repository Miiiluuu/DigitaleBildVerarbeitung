"""
    Aufgabe 2.7:
    Berechnet 2D Fouriertransformierte und das Leistungsspektrum des Bildes
    aus Aufgabe 1.1
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import Aufgabe_1_1

# TODO: Achsenbeschriftungen!


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


def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2,
                      unterueberschrift3, abszisse, ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.
    """
    fig = plt.figure(figsize=(10, 11))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(131)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # zweiter Subplot
    ax2 = fig.add_subplot(132)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # dritter Subplot
    ax3 = fig.add_subplot(133)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift3)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 1.5])
    return ax1, ax2, ax3


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation
    fourier_image, power, amplitude, phase = calculate_fourier(szinti)
    # Plots:
    ax1, ax2, ax3 = plot_vorbereitung('Fouriertransformation des Bildes ' +
                                      'aus Aufgabe 1.1', 'Leistungsspektrum',
                                      'Amplitudenbild', 'Phasenbild',
                                      '$ν_{x}/ν_{Sx}$', '$ν_{y}/ν_{Sy}$')
    # Leistungsspektrum
    ax1.imshow(power, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    ticks = np.linspace(-0.5, 0.5, 11)
    ax1.set_xticks(ticks)
    ax1.set_yticks(ticks)
    ax1.set_xticklabels(ticks, rotation=75)
    # Amplitudenbild
    ax2.imshow(amplitude, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    ax2.set_xticks(ticks)
    ax2.set_yticks(ticks)
    ax2.set_xticklabels(ticks, rotation=75)
    # Phasenbild
    ax3.imshow(phase, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    ax3.set_xticks(ticks)
    ax3.set_yticks(ticks)
    ax3.set_xticklabels(ticks, rotation=75)


if __name__ == "__main__":
    main()

# Interpretation:
    # Phasenbild codiert raeumliche Info
    # Linien entsprechen Aenderungen in Grauwerten / Farbspruenge / Kanten
    # gar keine Linien hier? keine Farbaenderungen?
