create table Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region)
);

create table Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_region foreign key (code_region) references Regions(code_region)
);


create table Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

--TODO Q4 Ajouter les créations des nouvelles tables

create table Commune(
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
    code_region INTEGER, -- Assurez-vous que la colonne code_region est correctement définie
    CONSTRAINT fk_travaux FOREIGN KEY (code_region) references Regions(code_region)
);

create table RealiseDans (
    code_departement INTEGER,
    id_travaux INTEGER,
    CONSTRAINT pk_RealiseDans PRIMARY KEY (code_departement),
);

create table Photovoltaique(
    puissance_instalée INTEGER,
    types_panneaux TEXT,
    CONSTRAINT ck_types_panneaux CHECK types_panneaux IN ('MONOCRISTALLIN', 'POLYCRISALLIN'),
    CONSTRAINT fk_photo FOREIGN KEY (code_departement)
);

create table Chauffage(
    energie_avant_travaux TEXT,
    energie_installé TEXT,
    generateur TEXT,
    type_chaudiere TEXT,
    CONSTRAINT ck_type_chaudiere CHECK type_chaudiere IN ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE'),
    CONSTRAINT ck_generateur CHECK generateur IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR'),
    CONSTRAINT ck_energie_avant_travaux CHECK energie_avant_travaux IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ'),
    CONSTRAINT ck_energie_installé CHECK energie_installé IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ'),
    CONSTRAINT fk_chauff FOREIGN KEY (code_departement)
);

create table Isolations(
    poste TEXT,
    isolant TEXT,
    epaisseur INTEGER,
    surface FLOAT,
    CONSTRAINT ck_poste CHECK poste IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE','RADIATEUR'),
    CONSTRAINT ck_isolant CHECK isolant IN ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES'),
    CONSTRAINT fk_isolant FOREIGN KEY (code_departement)
);




