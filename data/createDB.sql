CREATE TABLE Regions (
    code_region INTEGER,
    nom_region TEXT,
    CONSTRAINT pk_regions PRIMARY KEY (code_region)
);

CREATE TABLE Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    CONSTRAINT pk_departements PRIMARY KEY (code_departement),
    CONSTRAINT fk_region FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE
);

CREATE TABLE Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    CONSTRAINT pk_mesures PRIMARY KEY (code_departement, date_mesure),
    CONSTRAINT fk_mesures FOREIGN KEY (code_departement) REFERENCES Departements(code_departement) ON DELETE CASCADE
);

CREATE TABLE Commune(
    code_commune INTEGER,
    nom TEXT,
    status TEXT,
    altitude TEXT,
    population INTEGER,
    superficie INTEGER,
    code_canton INTEGER,
    code_arrondissement INTEGER,
    code_departement INTEGER,
    CONSTRAINT pk_commune PRIMARY KEY (code_commune, code_departement)
);

CREATE TABLE Travaux (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    cout_total_ht FLOAT,
    cout_induit_ht FLOAT,
    année INTEGER,
    type_logement TEXT,
    année_construction_logement INTEGER,
    code_region INTEGER,
    CONSTRAINT fk_travaux FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE
);
CREATE TABLE RealiseDans (
    code_departement INTEGER,
    id_travaux INTEGER,
    CONSTRAINT pk_RealiseDans PRIMARY KEY (code_departement)
);
CREATE TABLE Photovoltaique(
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    puissance_installee INTEGER,
    types_panneaux TEXT CHECK (types_panneaux IN ('MONOCRISTALLIN', 'POLYCRISALLIN')),
    CONSTRAINT fk_photo FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);

CREATE TABLE Chauffage(
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    energie_avant_travaux TEXT CHECK (energie_avant_travaux IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    energie_installe TEXT CHECK (energie_installe IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    generateur TEXT CHECK (generateur IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR')),
    type_chaudiere TEXT CHECK (type_chaudiere IN ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE')),
    CONSTRAINT fk_chauff FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);

CREATE TABLE Isolations(
	id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    poste TEXT CHECK (poste IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR')),
    isolant TEXT CHECK (isolant IN ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES')),
    epaisseur INTEGER,
    surface FLOAT,
    CONSTRAINT fk_isolant FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);
