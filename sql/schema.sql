-- Schéma de la base veloville (PostgreSQL 14+).
-- À compléter en respectant le contrat du sujet (types, clés, contraintes).
-- Le script doit être rejouable : prévoir les DROP ... IF EXISTS ou
-- CREATE TABLE IF NOT EXISTS.

-- ---------------------------------------------------------------
-- 1. Table station
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS station (
    -- ~ pour un regex en SQL
    station_id VARCHAR(10) PRIMARY KEY CHECK (station_id ~ '^S[0-9]{3}$'),
    nom VARCHAR(100) NOT NULL,
    commune VARCHAR(100) NOT NULL,
    capacite INTEGER NOT NULL CHECK (capacite > 0),
    latitude NUMERIC(8,5) NOT NULL,
    longitude NUMERIC(8,5) NOT NULL,
    date_mise_en_service DATE NOT NULL);

-- ---------------------------------------------------------------
-- 2. Table trajet
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS trajet (
    trajet_id VARCHAR(12) PRIMARY KEY CHECK (trajet_id ~ '^T[0-9]{6}$'),
    velo_id VARCHAR(8) NOT NULL CHECK (velo_id ~ '^V[0-9]{4}$'),
    depart_horodatage TIMESTAMP NOT NULL,
    station_depart VARCHAR(10) NOT NULL,
    station_arrivee VARCHAR(10),
    duree_secondes INTEGER NOT NULL CHECK (duree_secondes > 0),
    type_usager VARCHAR(20) NOT NULL CHECK (type_usager IN ('abonne', 'occasionnel')),
    usager_ref VARCHAR(9) CHECK (usager_ref ~ '^U[0-9A-Fa-f]{8}$'),
    CONSTRAINT fk_trajet_station_depart 
        FOREIGN KEY (station_depart)
        REFERENCES station(station_id),
    CONSTRAINT fk_trajet_station_arrivee
        FOREIGN KEY (station_arrivee)
        REFERENCES station(station_id),
    -- Un usager occasionnel ne porte pas de pseudonyme
    CONSTRAINT ck_trajet_usager_occasionnel
        CHECK (type_usager = 'abonne' OR usager_ref IS NULL));

-- ---------------------------------------------------------------
-- 3. Table incident
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS incident (
    incident_id VARCHAR(12) PRIMARY KEY CHECK (incident_id ~ '^I2026-[0-9]{4}$'),
    date_signalement TIMESTAMP NOT NULL,
    cible VARCHAR(20) NOT NULL CHECK (cible IN ('velo', 'station')),
    velo_id VARCHAR(8) CHECK (velo_id ~ '^V[0-9]{4}$'),
    station_id VARCHAR(10),
    type_incident VARCHAR(100) NOT NULL
        CHECK (
            type_incident IN (
                'vandalisme',
                'selle abimee',
                'eclairage HS',
                'chaine deraillee',
                'ecran borne illisible',
                'pneu creve',
                'frein defectueux',
                'borne hors service')),
    statut VARCHAR(20) NOT NULL CHECK (statut IN ('ouvert', 'en_cours', 'resolu')),
    date_resolution TIMESTAMP,
    technicien VARCHAR(100),
    CONSTRAINT fk_incident_station
        FOREIGN KEY (station_id)
        REFERENCES station(station_id),
    -- RG6 : exactement une référence, cohérente avec la cible
    CONSTRAINT ck_incident_cible
        CHECK ((cible = 'velo'
                AND velo_id IS NOT NULL
                AND station_id IS NULL)
            OR
            (   cible = 'station'
                AND station_id IS NOT NULL
                AND velo_id IS NULL)),
    -- RG8 : date présente si et seulement si l'incident est résolu
    CONSTRAINT ck_incident_resolution
        CHECK ((statut = 'resolu'
                AND date_resolution IS NOT NULL
                AND date_resolution >= date_signalement)
            OR
            (   statut IN ('ouvert', 'en_cours')
                AND date_resolution IS NULL)));

-- ---------------------------------------------------------------
-- 4. Table utilisateur
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('exploitant', 'direction')));

-- ---------------------------------------------------------------
-- 5. Index utiles aux filtres et aux indicateurs
-- ---------------------------------------------------------------
-- Filtrer les stations par commune
CREATE INDEX IF NOT EXISTS idx_station_commune ON station(commune);

-- Filtrer les trajets par période
CREATE INDEX IF NOT EXISTS idx_trajet_depart_horodatage ON trajet(depart_horodatage);

-- Filtrer par station et calculer les départs et arrivées
CREATE INDEX IF NOT EXISTS idx_trajet_station_depart ON trajet(station_depart);
CREATE INDEX IF NOT EXISTS idx_trajet_station_arrivee ON trajet(station_arrivee);

-- Filtrer les incidents par statut et les trier par date
CREATE INDEX IF NOT EXISTS idx_incident_statut_date ON incident(statut, date_signalement DESC);
