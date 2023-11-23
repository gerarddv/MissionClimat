import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db

class Window(tk.Toplevel):

    # Attributs de la classe (pour être en mesure de les utiliser dans les différentes méthodes)
    treeView = None
    input = None
    errorLabel = None
    region_combobox = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(600, 450, self)
        self.title('Q3 : départements pour une région donnée (version dynamique)')
        display.defineGridDisplay(self, 3, 3)
        self.grid_rowconfigure(3, weight=10) # On donne un poids plus important à la dernière ligne pour l'affichage du tableau
        ttk.Label(self, text="On a repris le code de F2. Modifier l'interface pour proposer un choix de la région sans saisie manuelle (par exemple un proposer un menu déroulant avec les valeurs extraites de la base, ou toute autre idée).",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0, columnspan=3)

        # Affichage du label, de la case de saisie et du bouton valider
        ttk.Label(self, text='Veuillez indiquer une région :', anchor="center", font=('Helvetica', '10', 'bold')).grid(row=1, column=0)

        # Création d'un Combobox pour afficher les régions extraites de la base
        regions = self.get_regions_from_database()  # Fonction à implémenter pour extraire les régions de la base
        self.region_combobox = ttk.Combobox(self, values=regions)
        self.region_combobox.grid(row=1, column=1)
        self.region_combobox.bind('<Return>', self.searchRegion)  # On bind l'appui de la touche entrée sur le Combobox

        ttk.Button(self, text='Valider', command=self.searchRegion).grid(row=1, column=2)

        # On place un label sans texte, il servira à afficher les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=2, sticky="we")

        # On prépare un treeView vide pour l'affichage de nos résultats
        columns = ('code_departement', 'nom_departement',)
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=3, sticky='nswe')

    # Fonction pour extraire les régions de la base de données
    def get_regions_from_database(self):
        try:
            cursor = db.data.cursor()
            result = cursor.execute("SELECT DISTINCT nom_region FROM Regions")
            regions = [row[0] for row in result.fetchall()]
            return regions
        except Exception as e:
            # Gérer l'erreur, par exemple, afficher un message d'erreur et renvoyer une liste vide
            print("Erreur lors de l'extraction des régions :", repr(e))
            return []

    # Fonction qui récupère la valeur sélectionnée, exécute la requête et affiche les résultats
    def searchRegion(self, event=None):
        # On vide le treeView (pour rafraîchir les données si quelque chose était déjà présent)
        self.treeView.delete(*self.treeView.get_children())

        # On récupère la valeur sélectionnée dans le Combobox
        region = self.region_combobox.get()

        # Si la sélection est vide, on affiche une erreur
        if len(region) == 0:
            self.errorLabel.config(foreground='red', text="Veuillez sélectionner une région !")
        else:
            try:
                cursor = db.data.cursor()
                result = cursor.execute("""SELECT code_departement, nom_departement
                                            FROM Departements JOIN Regions USING (code_region)
                                            WHERE nom_region = ?
                                            ORDER BY code_departement""", [region])

            except Exception as e:
                self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))
            else:
                # On affiche les résultats de la requête dans le tableau
                i = 0
                for row in result:
                    self.treeView.insert('', tk.END, values=row)
                    i += 1
                # On affiche un message à l'utilisateur en fonction du nombre de résultats de la requête
                if i == 0:
                    self.errorLabel.config(foreground='orange', text="Aucun résultat pour la région \"" + region + "\" !")
                else:
                    self.errorLabel.config(foreground='green', text="Voici les résultats pour la région \"" + region + "\" :")
