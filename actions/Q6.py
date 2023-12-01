import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1240, 720, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2018)')
        display.defineGridDisplay(self, 2, 1)

        temperature_query = """
                   SELECT strftime('%m', date_mesure) as mois, AVG(temperature_min_mesure) as moy_min
                   FROM Mesures
                   WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'
                   GROUP BY mois
                   ORDER BY mois;
               """

        temperature_result = self.execute_query(temperature_query)
        tabx = [row[0] for row in temperature_result]
        tabminmoy = [row[1] for row in temperature_result]

        # Fetch travaux data
        travaux_query = """
                   SELECT strftime('%m', date_travaux) as mois, SUM(cout_total_ht) as total_cout_travaux
                   FROM Travaux
                   WHERE strftime('%Y', date_travaux) = '2018'
                   GROUP BY mois
                   ORDER BY mois;
               """

        travaux_result = self.execute_query(travaux_query)
        tabx1 = [row[0] for row in travaux_result]
        tabcout = [row[1] for row in travaux_result]

        # Convert date strings to datetime objects
        datetime_dates = [datetime.strptime(date, '%m').strftime("%B") for date in tabx]
        datetime_dates1 = [datetime.strptime(date, '%m').strftime("%B") for date in tabx1]

        # Create a figure with dual y-axes
        fig, ax1 = plt.subplots(figsize=(15, 8))

        # axe y gauche temperature
        color = 'tab:blue'
        ax1.set_xlabel('Mois 2018')
        ax1.set_ylabel('Température Min Moyenne', color=color)
        ax1.plot(datetime_dates, tabminmoy, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        #axe y cout
        ax2 = ax1.twinx()
        color = 'tab:green'
        ax2.set_ylabel('Coût Total Travaux', color=color)
        ax2.plot(datetime_dates1, tabcout, color=color)
        ax2.tick_params(axis='y', labelcolor=color)


        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        plt.xticks(rotation='vertical')

        plt.show()

    def execute_query(self, query):
        try:
            cursor = db.data.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error: " + repr(e))


