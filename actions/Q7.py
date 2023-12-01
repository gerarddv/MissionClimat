import tkinter as tk
from utils import display
from tkinter import ttk
import sqlite3
from prettytable import PrettyTable
from utils import db
import calendar
from datetime import datetime

# Pointeur sur la base de données
data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.travaux_type_details_entered = False

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q7 : gérer les travaux de rénovation')
        display.defineGridDisplay(self, 2, 1)

        menu = tk.Menu(self)
        self.config(menu=menu)

        photovoltaique_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Photovoltaique", menu=photovoltaique_menu)
        photovoltaique_menu.add_command(label="Add Photovoltaique", command=self.add_photovoltaique)
        photovoltaique_menu.add_command(label="Modify Photovoltaique", command=self.modify_photovoltaique)
        photovoltaique_menu.add_command(label="Delete Photovoltaique", command=self.delete_photovoltaique)

        isolations_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Isolation", menu=isolations_menu)
        isolations_menu.add_command(label="Add Isolation", command=self.add_isolation)
        isolations_menu.add_command(label="Modify Isolation", command=self.modify_isolation)
        isolations_menu.add_command(label="Delete Isolation", command=self.delete_isolation)

        chauffage_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Chauffage", menu=chauffage_menu)
        chauffage_menu.add_command(label="Add Chauffage", command=self.add_chauffage)
        chauffage_menu.add_command(label="Modify Chauffage", command=self.modify_chauffage)
        chauffage_menu.add_command(label="Delete Chauffage", command=self.delete_chauffage)

    def close_display_window(self):
        # Destroy the display window
        if hasattr(self, 'display_window') and self.display_window:
            self.display_window.destroy()

    def display_table(self, table_name):
        cursor = data.cursor()
        query = "SELECT * FROM {}".format(table_name)
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            tk.messagebox.showinfo(table_name, "No data in the table.")
            return

        columns = [description[0] for description in cursor.description]

        table = PrettyTable(columns)
        for row in rows:
            table.add_row(row)

        display_window = tk.Toplevel(self)
        display_window.title(table_name)

        text_widget = tk.Text(display_window, wrap="none", height=20, width=80)
        text_widget.grid(row=0, column=0, padx=10, pady=10)

        text_widget.insert(tk.END, str(table))

        text_widget.config(state=tk.DISABLED)

    def get_max_travaux_id(self):
        try:
            cursor = data.cursor()
            query = "SELECT MAX(id_travaux) FROM Travaux"
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0  # Return 0 if no rows in the table
        except Exception as e:
            tk.messagebox.showerror("Error", "Failed to retrieve max id_travaux. Error: {}".format(str(e)))
            return 0
    def add_new_travaux(self):
        def insert_travaux_data(cout_total_ht, cout_induit_ht, date_travaux, type_logement, annee_construction_logement,
                                code_region):
            cursor = data.cursor()
            max_trav = self.get_max_travaux_id()
            query = """
                UPDATE Travaux 
                SET 
                    cout_total_ht = {},
                    cout_induit_ht = {},
                    date_travaux = '{}',
                    type_logement = '{}',
                    annee_construction_logement = '{}',
                    code_region = {}
                WHERE 
                    id_travaux = {}
                """.format(cout_total_ht, cout_induit_ht, date_travaux, type_logement,
                           annee_construction_logement, code_region, max_trav)
            cursor.execute(query)
            data.commit()
            self.travaux_type_details_entered = False
            tk.messagebox.showinfo("Success", "New travaux added successfully!")

        # Create labels and entry widgets for each attribute
        labels = ["cout_total_ht:", "cout_induit_ht:", "date_travaux:", "type_logement:",
                  "annee_construction_logement:", "code_region:"]
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")

            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")

            entries.append(entry)

        # Validate button
        validate_button = ttk.Button(self, text="Add Travaux", command=lambda: insert_travaux_data(
            *map(lambda entry: entry.get(), entries)
        ))
        validate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def add_photovoltaique(self):
        def insert_data(puissance_installee, types_panneaux):
            try:
                cursor = data.cursor()
                # Step 1: Insert into Travaux
                query0 = ("INSERT INTO Travaux (id_travaux, date_travaux) VALUES ({}, '{}')".format(self.get_max_travaux_id() + 1,
                    datetime.now().date()))
                cursor.execute(query0)
                data.commit()
                # Step 2: Get the id_travaux of the newly inserted row
                cursor.execute("SELECT last_insert_rowid()")
                max_travaux_id = cursor.fetchone()[0]
                # Step 3: Insert into Photovoltaique using the obtained id_travaux
                query = "INSERT INTO Photovoltaique (id_travaux, puissance_installee, types_panneaux) VALUES ({}, {}, '{}')".format(
                    max_travaux_id, puissance_installee, types_panneaux)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data inserted successfully!")
                destroy_photovoltaique_widgets()
                self.add_new_travaux()
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to insert data. Error: {}".format(str(e)))
        def destroy_photovoltaique_widgets():
            # Destroy Photovoltaique entry form widgets
            label_puissance_installee.destroy()
            puissance_installee_entry.destroy()
            label_types_panneaux.destroy()
            types_panneaux_dropdown.destroy()
            validate_button.destroy()

        types_panneaux_options = ['MONOCRISTALLIN', 'POLYCRISTALLIN']

        # puissance_installee
        label_puissance_installee = ttk.Label(self, text="Puissance Installee:")
        label_puissance_installee.grid(row=0, column=0, pady=5, padx=10, sticky="e")
        puissance_installee_entry = ttk.Entry(self)
        puissance_installee_entry.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        # types_panneaux
        label_types_panneaux = ttk.Label(self, text="Types Panneaux:")
        label_types_panneaux.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        selected_types_panneaux = tk.StringVar()
        types_panneaux_dropdown = ttk.Combobox(self, textvariable=selected_types_panneaux,
                                               values=types_panneaux_options)
        types_panneaux_dropdown.set(types_panneaux_options[0])  # Set the default value
        types_panneaux_dropdown.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        validate_button = ttk.Button(self, text="Validate", command=lambda: insert_data(puissance_installee_entry.get(),
                                                                                        selected_types_panneaux.get()))
        validate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def modify_photovoltaique(self):
        def update_data(id_travaux, puissance_installee, types_panneaux):
            try:
                cursor = data.cursor()
                query = """UPDATE Photovoltaique
                           SET puissance_installee = {},
                               types_panneaux = '{}'
                           WHERE id_travaux = {}""".format(puissance_installee, types_panneaux, id_travaux)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data updated successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to update data. Error: {}".format(str(e)))

        types_panneaux_options = ['MONOCRISTALLIN', 'POLYCRISTALLIN']

        # Display the corresponding table entries
        self.display_table("Photovoltaique")

        # Ask the user for the id_travaux to update
        id_travaux_to_update = tk.simpledialog.askinteger("Modify Photovoltaique", "Enter id_travaux to modify:")

        # Get the existing data for the specified id_travaux
        cursor = data.cursor()
        query = "SELECT * FROM Photovoltaique WHERE id_travaux = {}".format(id_travaux_to_update)
        cursor.execute(query)
        existing_data = cursor.fetchone()

        if not existing_data:
            tk.messagebox.showinfo("Error", "No data found for id_travaux {}".format(id_travaux_to_update))
            return

        # Create labels and entry/dropdown widgets for each attribute
        labels = ["Puissance Installee:", "Types Panneaux:"]
        default_values = existing_data[1:]  # Skip id_travaux
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")

            if label_text == "Puissance Installee:":
                entry = ttk.Entry(self)
                entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entry.insert(0, default_values[i])  # Set the default value
            elif label_text == "Types Panneaux:":
                selected_types_panneaux = tk.StringVar()
                types_panneaux_dropdown = ttk.Combobox(self, textvariable=selected_types_panneaux,
                                                       values=types_panneaux_options)
                types_panneaux_dropdown.set(default_values[i])  # Set the default value
                types_panneaux_dropdown.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entries.append(types_panneaux_dropdown)

        # Validate button
        validate_button = ttk.Button(self, text="Validate", command=lambda: update_data(
            id_travaux_to_update,
            entry.get(),
            selected_types_panneaux.get()  # Add the missing argument here
        ))
        validate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


    def delete_photovoltaique(self):
        def delete_data(id_travaux):
            cursor = data.cursor()
            query = "DELETE FROM Photovoltaique WHERE id_travaux = {}".format(id_travaux)
            cursor.execute(query)
            travaux_query = "DELETE FROM Travaux WHERE id_travaux = {}".format(id_travaux)
            cursor.execute(travaux_query)
            data.commit()

        self.display_table("Photovoltaique")

        id_travaux_to_delete = tk.simpledialog.askinteger("Delete Photovoltaique", "Enter id_travaux to delete:")

        confirmation = tk.messagebox.askyesno("Confirmation",
                                           "Voulez vous supprimer la ligne Photovoltaique avec id_travaux {}?".format(
                                               id_travaux_to_delete))

        if confirmation:
            delete_data(id_travaux_to_delete)
            self.close_display_window()

    def add_isolation(self):
        def insert_data(poste, isolant, epaisseur, surface):
            try:
                cursor = data.cursor()
                # Step 1: Insert into Travaux
                query0 = ("INSERT INTO Travaux (id_travaux, date_travaux) VALUES ({}, '{}')".format(
                    self.get_max_travaux_id() + 1,
                    datetime.now().date()))
                cursor.execute(query0)
                data.commit()
                # Step 2: Get the id_travaux of the newly inserted row
                cursor.execute("SELECT last_insert_rowid()")
                max_travaux_id = cursor.fetchone()[0]
                query = "INSERT INTO Isolations (id_travaux,poste, isolant, epaisseur, surface) VALUES ({},'{}', '{}', {}, {})".format(
                    max_travaux_id, poste, isolant, epaisseur, surface)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data inserted successfully!")
                destroy_isolation_widgets()
                self.add_new_travaux()
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to insert data. Error: {}".format(str(e)))

        def destroy_isolation_widgets():
            label_poste.destroy()
            poste_dropdown.destroy()
            label_isolant.destroy()
            isolant_dropdown.destroy()
            label_epaisseur.destroy()
            epaisseur_entry.destroy()
            label_surface.destroy()
            surface_entry.destroy()
            validate_button.destroy()

        poste_options = ['COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING', 'TOITURE TERASSE', 'PLANCHER BAS']
        isolant_options = ['AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES']

        #poste
        label_poste = ttk.Label(self, text="Poste:")
        label_poste.grid(row=0, column=0, pady=5, padx=10, sticky="e")
        selected_poste = tk.StringVar()
        poste_dropdown = ttk.Combobox(self, textvariable=selected_poste, values=poste_options)
        poste_dropdown.set(poste_options[0])  # Set the default value
        poste_dropdown.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        #isolant
        label_isolant = ttk.Label(self, text="Isolant:")
        label_isolant.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        selected_isolant = tk.StringVar()
        isolant_dropdown = ttk.Combobox(self, textvariable=selected_isolant, values=isolant_options)
        isolant_dropdown.set(isolant_options[0])  # Set the default value
        isolant_dropdown.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        #epaisseur
        label_epaisseur = ttk.Label(self, text="Epaisseur:")
        label_epaisseur.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        epaisseur_entry = ttk.Entry(self)
        epaisseur_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        epaisseur_entry.insert(0, 0)  # Set the default value

        #surface
        label_surface = ttk.Label(self, text="Surface:")
        label_surface.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        surface_entry = ttk.Entry(self)
        surface_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        surface_entry.insert(0, 0)  # Set the default value

        # Validate
        validate_button = ttk.Button(self, text="Validate", command=lambda: insert_data( selected_poste.get(),
            selected_isolant.get(), float(epaisseur_entry.get()),float(surface_entry.get())))
        validate_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def modify_isolation(self):
        def update_data(id_travaux, poste, isolant, epaisseur, surface):
            try:
                cursor = data.cursor()
                query = """UPDATE Isolations
                           SET poste = '{}',
                               isolant = '{}',
                               epaisseur = {},
                               surface = {}
                           WHERE id_travaux = {}""".format(poste, isolant, epaisseur, surface, id_travaux)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data updated successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to update data. Error: {}".format(str(e)))

        poste_options = ['COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING', 'TOITURE TERASSE', 'PLANCHER BAS']
        isolant_options = ['AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES']

        # Display the corresponding table entries
        self.display_table("Isolations")

        # Ask the user for the id_travaux to update
        id_travaux_to_update = tk.simpledialog.askinteger("Modify Isolation", "Enter id_travaux to modify:")

        # Get the existing data for the specified id_travaux
        cursor = data.cursor()
        query = "SELECT * FROM Isolations WHERE id_travaux = {}".format(id_travaux_to_update)
        cursor.execute(query)
        existing_data = cursor.fetchone()

        if not existing_data:
            tk.messagebox.showinfo("Error", "No data found for id_travaux {}".format(id_travaux_to_update))
            return

        # Create labels and entry/dropdown widgets for each attribute
        labels = ["Poste:", "Isolant:", "Epaisseur:", "Surface:"]
        default_values = existing_data[1:]  # Skip id_travaux
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")

            if label_text == "Poste:":
                selected_poste = tk.StringVar()
                poste_dropdown = ttk.Combobox(self, textvariable=selected_poste, values=poste_options)
                poste_dropdown.set(default_values[i])  # Set the default value
                poste_dropdown.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entries.append(poste_dropdown)
            elif label_text == "Isolant:":
                selected_isolant = tk.StringVar()
                isolant_dropdown = ttk.Combobox(self, textvariable=selected_isolant, values=isolant_options)
                isolant_dropdown.set(default_values[i])  # Set the default value
                isolant_dropdown.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entries.append(isolant_dropdown)
            else:
                entry = ttk.Entry(self)
                entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entry.insert(0, str(default_values[i]))  # Set the default value as a string
                entries.append(entry)

        # Validate button
        validate_button = ttk.Button(self, text="Validate", command=lambda: update_data(id_travaux_to_update,
            *map(lambda entry: entry.get() if isinstance(entry, tk.Entry) else entry.get(), entries)))
        validate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        # Center the labels and entries in their respective columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def delete_isolation(self):
        def delete_data(id_travaux):
            cursor = data.cursor()
            query = "DELETE FROM Isolations WHERE id_travaux = {}".format(id_travaux)
            cursor.execute(query)
            travaux_query = "DELETE FROM Travaux WHERE id_travaux = {}".format(id_travaux)
            cursor.execute(travaux_query)
            data.commit()

        self.display_table("Isolations")

        #id_travaux to delete
        id_travaux_to_delete = tk.simpledialog.askinteger("Delete Isolation", "Enter id_travaux to delete:")


        confirmation = tk.messagebox.askyesno("Confirmation",
                                           "Voulez vous supprimer la ligne Isolation avec id_travaux {}?".format(
                                               id_travaux_to_delete))
        if confirmation:
            delete_data(id_travaux_to_delete)
            self.close_display_window()

    def add_chauffage(self):
        def insert_data(energie_avant_travaux, energie_installe, generateur, type_chaudiere):
            try:
                cursor = data.cursor()
                # Step 1: Insert into Travaux
                query0 = ("INSERT INTO Travaux (id_travaux, date_travaux) VALUES ({}, '{}')".format(
                    self.get_max_travaux_id() + 1,
                    datetime.now().date()))
                cursor.execute(query0)
                data.commit()
                # Step 2: Get the id_travaux of the newly inserted row
                cursor.execute("SELECT last_insert_rowid()")
                max_travaux_id = cursor.fetchone()[0]
                query = "INSERT INTO Chauffage (id_travaux,energie_avant_travaux, energie_installe, generateur, type_chaudiere) VALUES ({},'{}', '{}', '{}', '{}')".format(
                    max_travaux_id,energie_avant_travaux, energie_installe, generateur, type_chaudiere)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data inserted successfully!")
                destroy_chauffage_widgets()
                self.add_new_travaux()
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to insert data. Error: {}".format(str(e)))

        def destroy_chauffage_widgets():
            label_energie_avant_travaux.destroy()
            energie_avant_travaux_dropdown.destroy()
            label_energie_installe.destroy()
            energie_installe_dropdown.destroy()
            label_generateur.destroy()
            generateur_dropdown.destroy()
            label_type_chaudiere.destroy()
            type_chaudiere_dropdown.destroy()
            validate_button.destroy()

        type_energie = ['AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ']
        generateur_options = ['AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE', 'RADIATEUR']
        type_chaudiere_options = ['STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE']

        #energie_avant_travaux
        label_energie_avant_travaux = ttk.Label(self, text="Energie Avant Travaux:")
        label_energie_avant_travaux.grid(row=0, column=0, pady=5, padx=10, sticky="e")
        selected_energie_avant_travaux = tk.StringVar()
        energie_avant_travaux_dropdown = ttk.Combobox(self, textvariable=selected_energie_avant_travaux,
                                                      values=type_energie)
        energie_avant_travaux_dropdown.set(type_energie[0])  # Set the default value
        energie_avant_travaux_dropdown.grid(row=0, column=1, pady=5, padx=10, sticky="w")

        #energie_installe
        label_energie_installe = ttk.Label(self, text="Energie Installe:")
        label_energie_installe.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        selected_energie_installe = tk.StringVar()
        energie_installe_dropdown = ttk.Combobox(self, textvariable=selected_energie_installe,
                                                 values=type_energie)
        energie_installe_dropdown.set(type_energie[0])  # Set the default value
        energie_installe_dropdown.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        #generateur
        label_generateur = ttk.Label(self, text="Generateur:")
        label_generateur.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        selected_generateur = tk.StringVar()
        generateur_dropdown = ttk.Combobox(self, textvariable=selected_generateur, values=generateur_options)
        generateur_dropdown.set(generateur_options[0])  # Set the default value
        generateur_dropdown.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        #type_chaudiere
        label_type_chaudiere = ttk.Label(self, text="Type Chaudiere:")
        label_type_chaudiere.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        selected_type_chaudiere = tk.StringVar()
        type_chaudiere_dropdown = ttk.Combobox(self, textvariable=selected_type_chaudiere,
                                               values=type_chaudiere_options)
        type_chaudiere_dropdown.set(type_chaudiere_options[0])  # Set the default value
        type_chaudiere_dropdown.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Validate
        validate_button = ttk.Button(self, text="Validate", command=lambda: insert_data(selected_energie_avant_travaux.get(), selected_energie_installe.get(),
            selected_generateur.get(), selected_type_chaudiere.get()))
        validate_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def modify_chauffage(self):
        def update_data(id_travaux, energie_avant_travaux, energie_installe, generateur, type_chaudiere):
            try:
                cursor = data.cursor()
                query = """UPDATE Chauffage
                           SET energie_avant_travaux = '{}',
                               energie_installe = '{}',
                               generateur = '{}',
                               type_chaudiere = '{}'
                           WHERE id_travaux = {}""".format(energie_avant_travaux, energie_installe, generateur,
                                                           type_chaudiere, id_travaux)
                cursor.execute(query)
                data.commit()
                tk.messagebox.showinfo("Success", "Data updated successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", "Failed to update data. Error: {}".format(str(e)))

        type_energie_options = ['AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ']
        generateur_options = ['AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE', 'RADIATEUR']
        type_chaudiere_options = ['STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE']
        types = [type_energie_options, type_energie_options,generateur_options,type_chaudiere_options]

        # Display the corresponding table entries
        self.display_table("Chauffage")

        # Ask the user for the id_travaux to update
        id_travaux_to_update = tk.simpledialog.askinteger("Modify Chauffage", "Enter id_travaux to modify:")

        # Get the existing data for the specified id_travaux
        cursor = data.cursor()
        query = "SELECT * FROM Chauffage WHERE id_travaux = {}".format(id_travaux_to_update)
        cursor.execute(query)
        existing_data = cursor.fetchone()

        if not existing_data:
            tk.messagebox.showinfo("Error", "No data found for id_travaux {}".format(id_travaux_to_update))
            return

        # Create labels and entry/dropdown widgets for each attribute
        labels = ["Energie Avant Travaux:", "Energie Installe:", "Generateur:", "Type Chaudiere:"]
        default_values = existing_data[1:]  # Skip id_travaux
        entries = []

        for i, label_text in enumerate(labels):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")

            selected_option = tk.StringVar()
            dropdown_menu = ttk.Combobox(self, textvariable=selected_option, values=types[i])
            dropdown_menu.set(default_values[i])  # Set the default value
            dropdown_menu.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            entries.append(dropdown_menu)


        # Validate button
        validate_button = ttk.Button(self, text="Validate", command=lambda: update_data(id_travaux_to_update,
            *map(lambda entry: entry.get() if isinstance(entry, tk.Entry) else entry.get(), entries)))
        validate_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)



    def delete_chauffage(self):
        def delete_data(id_travaux):
            cursor = data.cursor()
            query = "DELETE FROM Chauffage WHERE id_travaux = {}".format(id_travaux)
            cursor.execute(query)
            data.commit()

        self.display_table("Chauffage")

        #id_travaux to delete
        id_travaux_to_delete = tk.simpledialog.askinteger("Delete Chauffage", "Enter id_travaux to delete:")

        confirmation = tk.messagebox.askyesno("Confirmation",
                                           "Voulez vous supprimer la ligne Chauffage avec id_travaux {}?".format(
                                               id_travaux_to_delete))

        if confirmation:
            delete_data(id_travaux_to_delete)
            self.close_display_window()

    def get_travaux_from_database(self):
        try:
            cursor = db.data.cursor()
            result = cursor.execute("SELECT id_travaux FROM Regions")
            regions = [row[0] for row in result.fetchall()]
            return regions
        except Exception as e:
            # Gérer l'erreur, par exemple, afficher un message d'erreur et renvoyer une liste vide
            print("Erreur lors de l'extraction des régions :", repr(e))
            return []

