"""
    Aufgabe 2.2:
    Erstellt das Grauwerthistogramm des Bildes aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1


def erstelle_grauwerthistogramm_log(ueberschrift, unterueberschrift,
                                abszisse, ordinate, werte):
    """ Erstellung Grauwertprofil mit entsprechenden Ueberschriften, 
        Achsenbeschriftung, logarithmischer Skaleneinteilung etc.
         Parameter:
        ----------
        werte: Array, Eingabewerte.
    """
    fig1 = plt.figure(figsize=(10, 5))
    # Hinzufuegen der Ueberschrift zum Plot
    fig1.suptitle(ueberschrift, fontsize=20)
    # Hinzufuegen einer Unterueberschrift
    ax = fig1.add_subplot(111)
    # Position der Unterueberschrift festlegen
    fig1.subplots_adjust(top=0.80)
    # Beschriftung der Unterueberschrift
    ax.set_title(unterueberschrift, fontsize=15)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    plt.hist(werte, bins=256, density=True, log=True)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    plt.show()


def erstelle_grauwerthistogramm_abgeschnitten(ueberschrift, unterueberschrift,
                                               abszisse, ordinate, werte):
    """ Erstellung Grauwertprofil mit entsprechenden Ueberschriften,
        Achsenbeschriftung etc. Ordinate ist zur besseren Darstellung
        kleinerer Werte abgeschnitten.
        
        Parameter:
        ----------
        werte: Array, Eingabewerte.
    """    
    fig2 = plt.figure(figsize=(10, 5))
    # Hinzufuegen der Ueberschrift zum Plot
    fig2.suptitle(ueberschrift, fontsize=20)
    # Hinzufuegen einer Unterueberschrift
    ax = fig2.add_subplot(111)
    # Position der Unterueberschrift festlegen
    fig2.subplots_adjust(top=0.80)
    # Beschriftung der Unterueberschrift
    ax.set_title(unterueberschrift, fontsize=15)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    ordinate, _, _ = plt.hist(werte, bins=256, density=True)
    # Ordinatenwerte sortieren
    ordinate_sort = np.sort(ordinate)
    # Ordinatenachse kuerzen
    plt.ylim(0, ordinate_sort[-2] * 1.1)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    plt.show()
    

def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Grauwerthistogramm zeichnen:
    # logarithmische Skaleneinteilung
    erstelle_grauwerthistogramm_log('Grauwerthistogramm',
                                'fuer Bild aus Aufgabe 1.1, ' +
                                'logarithmische Skala', r'$f$',
                                'Häufigkeitsverteilung $h(f)$',
                                szinti.flatten())
    # Ordinatenachse gekuerzt
    erstelle_grauwerthistogramm_abgeschnitten('Grauwerthistogramm',
                                'fuer Bild aus Aufgabe 1.1, ' +
                                'gekuerzte Ordinatenachse', r'$f$',
                                'Häufigkeitsverteilung $h(f)$',
                                szinti.flatten())


if __name__ == "__main__":
    main()

