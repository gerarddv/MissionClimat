import tkinter as tk
from tkinter import ttk
from utils import display

class Window(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 500, self)
        self.title('Consultation des données de la base')
        display.defineGridDisplay(self, 1, 1)

        tables = [
            {'name': 'Regions', 'columns': ('code_region', 'nom_region'),
             'query': 'SELECT code_region, nom_region FROM Regions ORDER BY code_region'},
            {'name': 'Departements',
             'columns': ('code_departement', 'nom_departement', 'code_region', 'zone_climatique'),
             'query': 'SELECT code_departement, nom_departement, code_region, zone_climatique FROM Departements ORDER BY code_departement'},
            {'name': 'Mesures', 'columns': (
            'code_departement', 'date_mesure', 'temperature_min_mesure', 'temperature_max_mesure',
            'temperature_moy_mesure'),
             'query': 'SELECT code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure FROM Mesures ORDER BY date_mesure LIMIT 1,1000'},
            {'name': 'Commune', 'columns': (
            'code_commune', 'nom', 'status', 'altitude', 'population', 'superficie', 'code_canton',
            'code_arrondissement', 'code_departement'),
             'query': 'SELECT code_commune, nom, status, altitude, population, superficie, code_canton, code_arrondissement, code_departement FROM Commune ORDER BY code_commune, code_departement'},
            {'name': 'Travaux', 'columns': (
            'id_travaux', 'cout_total_ht', 'cout_induit_ht', 'année', 'type_logement', 'année_construction_logement',
            'code_region'),
             'query': 'SELECT id_travaux, cout_total_ht, cout_induit_ht, année, type_logement, année_construction_logement, code_region FROM Travaux ORDER BY id_travaux'},
            {'name': 'RealiseDans', 'columns': ('code_departement', 'id_travaux'),
             'query': 'SELECT code_departement, id_travaux FROM RealiseDans ORDER BY code_departement'},
            {'name': 'Photovoltaique', 'columns': ('id_travaux', 'puissance_installee', 'types_panneaux'),
             'query': 'SELECT id_travaux, puissance_installee, types_panneaux FROM Photovoltaique ORDER BY id_travaux'},
            {'name': 'Chauffage',
             'columns': ('id_travaux', 'energie_avant_travaux', 'energie_installe', 'generateur', 'type_chaudiere'),
             'query': 'SELECT id_travaux, energie_avant_travaux, energie_installe, generateur, type_chaudiere FROM Chauffage ORDER BY id_travaux'},
            {'name': 'Isolations', 'columns': ('id_travaux', 'poste', 'isolant', 'epaisseur', 'surface'),
             'query': 'SELECT id_travaux, poste, isolant, epaisseur, surface FROM Isolations ORDER BY id_travaux'}
        ]

        # Définition des onglets
        #TODO Q4 Créer des nouveaux onglets pour les nouvelles tables
        self.create_tabs(tables)

    def create_tabs(self, tables):
        tabControl = ttk.Notebook(self)

        for table in tables:
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=table['name'])

            display.defineGridDisplay(tab, 1, 2)

            columns = table['columns']
            query = table['query']

            tree = display.createTreeViewDisplayQuery(tab, columns, query)
            scrollbar = ttk.Scrollbar(tab, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.grid(row=0, sticky="nswe")
            scrollbar.grid(row=0, column=1, sticky="ns")

        tabControl.grid(row=0, column=0, sticky="nswe")

        #TODO Q4 Afficher les données des nouvelles tables