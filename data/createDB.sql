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

CREATE TABLE IF NOT EXISTS Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    CONSTRAINT pk_mesures PRIMARY KEY (code_departement, date_mesure),
    CONSTRAINT fk_mesures FOREIGN KEY (code_departement) REFERENCES Departements(code_departement) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Commune(
    code_commune TEXT,
    nom TEXT,
    status TEXT,
    altitude FLOAT,
    population FLOAT,
    superficie FLOAT,
    code_canton INTEGER,
    code_arrondissement INTEGER,
    code_departement TEXT,
    CONSTRAINT pk_commune PRIMARY KEY (code_commune, code_departement)
);

CREATE TABLE IF NOT EXISTS Travaux (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    cout_total_ht FLOAT,
    cout_induit_ht FLOAT,
    annee_travaux TEXT,
    type_logement TEXT,
    annee_construction_logement TEXT,
    code_region INTEGER,
    CONSTRAINT fk_travaux FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS RealiseDans (
    code_departement INTEGER,
    id_travaux INTEGER,
    CONSTRAINT pk_RealiseDans PRIMARY KEY (code_departement)
);
CREATE TABLE IF NOT EXISTS Photovoltaique(
    id_travaux INTEGER PRIMARY KEY,
    puissance_installee FLOAT,
    types_panneaux TEXT CHECK (types_panneaux IN ('MONOCRISTALLIN', 'POLYCRISTALLIN')),
    CONSTRAINT fk_photo FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Chauffage(
    id_travaux INTEGER PRIMARY KEY,
    energie_avant_travaux TEXT CHECK (energie_avant_travaux IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    energie_installe TEXT CHECK (energie_installe IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    generateur TEXT CHECK (generateur IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR')),
    type_chaudiere TEXT CHECK (type_chaudiere IN ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE')),
    CONSTRAINT fk_chauff FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Isolations(
	id_travaux INTEGER PRIMARY KEY,
    poste TEXT CHECK (poste IN ('COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING','TOITURE TERASSE', 'PLANCHER BAS')),
    isolant TEXT CHECK (isolant IN ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES')),
    epaisseur FLOAT,
    surface FLOAT,
    CONSTRAINT fk_isolant FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux) ON DELETE CASCADE
);

-- Création du trigger
-- CREATE TRIGGER IF NOT EXISTS trigger_check_code_commune
-- BEFORE INSERT ON Commune
-- FOR EACH ROW
-- WHEN NEW.code_commune IS NULL OR NOT typeof(NEW.code_commune) = 'integer'
-- BEGIN
--     -- Remplacer le code_commune par 97 si ce n'est pas un entier
--     UPDATE Commune SET code_commune = 97 WHERE NEW.code_commune IS NULL OR NOT typeof(NEW.code_commune) = 'integer';
-- END;

