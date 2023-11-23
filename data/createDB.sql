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
    code_arromatizey INTEGER,
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



CREATE TABLE Photovoltaique(
    puissance_instalee INTEGER,
    type_panneaux TEXT,
    CONSTRAINT ck_types_panneaux CHECK types_panneaux IN ('MONOCRISTALLIN', 'POLYCRISALLIN'),
    CONSTRAINT fk_photo FOREIGN KEY (code_departement) REFERENCES Departements(code_departement) ON DELETE CASCADE
);

CREATE TABLE Chauffage(
    energie_avant_travaux TEXT,
    energie_installe TEXT,
    generateur TEXT,
    type_chaudiere TEXT,
    CONSTRAINT ck_type_chaudiere CHECK type_chaudiere IN ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE'),
    CONSTRAINT ck_generateur CHECK generateur IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR'),
    CONSTRAINT ck_energie_avant_travaux CHECK energie_avant_travaux IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ'),
    CONSTRAINT ck_energie_installe CHECK energie_installe IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ'),
    CONSTRAINT fk_chauff FOREIGN KEY (code_departement) REFERENCES Departements(code_departement) ON DELETE CASCADE
);

CREATE TABLE Isolations(
    poste TEXT,
    isolant TEXT,
    epaisseur INTEGER,
    surface FLOAT,
    CONSTRAINT ck_poste CHECK poste IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR'),
    CONSTRAINT ck_isolant CHECK isolant IN ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES'),
    CONSTRAINT fk_isolant FOREIGN KEY (code_departement) REFERENCES Departements(code_departement) ON DELETE CASCADE
);
