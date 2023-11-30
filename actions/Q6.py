import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2022)')
        display.defineGridDisplay(self, 2, 1)

        query = "SELECT strftime('%m', date_mesure) as mois, AVG(temperature_min_mesure) as moy_min " \
                "FROM Mesures" \
                "WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'" \
                "GROUP BY mois" \
                "ORDER BY mois;"

        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))
        tabmois = []  # abscisses
        tabminmoy = []
        for row in result:
            tabmois.append(row[0])
            tabminmoy.append(row[0])

        query = "SELECT strftime('%m', date_travaux) as mois, SUM(cout_total_ht) as total_cout_travaux " \
                "FROM Travaux " \
                "WHERE strftime('%Y', date_travaux) = '2018' " \
                "GROUP BY mois " \
                "ORDER BY mois;"
        result1 = []
        try:
            cursor = db.data.cursor()
            result1 = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))
        tabmois1 = []  # abscisses
        tabcout = []
        for row in result1:
            tabmois1.append(row[0])
            tabcout.append(row[0])

        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Plot des températures minimales moyennes
        plot1.plot(range(len(tabmois)), tabminmoy, color='b', label='temp min moyenne')
        # Ajout de la deuxième série de données sur le même subplot
        plot1.plot(range(len(tabmois1)), tabcout, color='g', label='cout total travaux')

        plot1.set_xlabel('Mois')
        plot1.set_ylabel('Température Min Moyenne / Coût Total Travaux')

        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
