import tkinter as tk
from utils import display
from tkinter import ttk
from utils import db

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2022)')
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(self, text="""Pour l’Isère et l'année 2022, donner deux courbes sur le même graphique  :
   - par mois, l’évolution de la moyenne des températures minimales
   - par mois, l’évolution des totaux de coûts de travaux tout type confondu""",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)

    def extract_data_temp(self):
        try:
            query = "SELECT strftime('%m', date_mesure) as mois, AVG(temperature_min_mesure) FROM Mesures" \
                    "WHERE code_departement = '38' AND strftime('%Y, dat_mesure) = '2022'" \
                    "GROUP BY mois" \
                    "ORDER BY mois;"
            cursor = db.data.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except Exception as e:
            print("Erreur : " + repr(e))
        return result

    def extract_data_cout(self):
        try:
            query = "SELECT strftime('%m', date_travaux) as mois, SUM(cout_travaux) as total_cout_travaux " \
                    "FROM Travaux " \
                    "WHERE strftime('%Y', date_travaux) = '2022' " \
                    "GROUP BY mois " \
                    "ORDER BY mois;"
            cursor = db.data.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except Exception as e:
            print("Erreur : " + repr(e))
        return result
    def show_graph_evolution(self):
        result = self.extract_data_temp()
        for row in result:
            print(row)

        result = self.extract_data_cout()
        for row in result:
            print(row)


    show_graph_evolution()