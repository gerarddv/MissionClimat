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
        display.centerWindow(1920, 1080, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2018)')
        display.defineGridDisplay(self, 2, 1)

        query = """
            SELECT strftime('%m', date_mesure) as mois, AVG(temperature_min_mesure) as moy_min
            FROM Mesures
            WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'
            GROUP BY mois
            ORDER BY mois;
        """

        result = []
        try:
            cursor = db.data.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            print("Erreur : " + repr(e))

        tabx = []  # abscisses
        tabminmoy = []
        for row in result:
            tabx.append(row[0])
            tabminmoy.append(row[1])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%m') for date in tabx]

        query = """
            SELECT date_travaux as mois, SUM(cout_total_ht) as total_cout_travaux
            FROM Travaux
            WHERE strftime('%Y', date_travaux) = '2018'
            GROUP BY mois;
        """

        result1 = []
        try:
            cursor = db.data.cursor()
            cursor.execute(query)
            result1 = cursor.fetchall()
        except Exception as e:
            print("Erreur : " + repr(e))

        tabx1 = []  # abscisses
        tabcout = []
        for row in result1:
            tabx1.append(row[0])
            tabcout.append(row[1])

        datetime_dates1 = [datetime.strptime(date, '%m') for date in tabx1]

        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Plot des températures minimales moyennes
        plot1.plot(range(len(datetime_dates)), tabminmoy, color='blue', label='temp min moyenne')
        # Ajout de la deuxième série de données sur le même subplot
        plot1.plot(range(len(datetime_dates1)), tabcout, color='green', label='cout total travaux')

        plot1.set_xlabel('Mois')
        plot1.set_ylabel('Température Min Moyenne', color='blue')  # Couleur associée à la première série de données

        # Création d'une deuxième échelle y pour le deuxième jeu de données
        plot2 = plot1.twinx()
        plot2.set_ylabel('Coût Total Travaux', color='green')  # Couleur associée à la deuxième série de données

        plot1.legend(loc='upper left')
        plot2.legend(loc='upper right')

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

