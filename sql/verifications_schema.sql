-- Exécuter un seul cas à la fois
-- après chaque exécuter ROLLBACK

-- ---------------------------------------------------------------
-- Vérifier les comptes
-- Attendu : exploitant01/exploitant et direction01/direction
-- ---------------------------------------------------------------

SELECT id_utilisateur, username, role
FROM utilisateur
ORDER BY id_utilisateur;

-- ---------------------------------------------------------------
-- Vérifier les permissions
-- Attendu : true dans les trois colonnes pour chaque table
-- ---------------------------------------------------------------

SELECT
    nom_table,
    has_table_privilege('veloville', nom_table, 'SELECT') AS lecture,
    has_table_privilege('veloville', nom_table, 'INSERT') AS insertion,
    has_table_privilege('veloville', nom_table, 'UPDATE') AS modification
FROM (
    VALUES
        ('public.station'),
        ('public.trajet'),
        ('public.incident'),
        ('public.utilisateur')
) AS tables(nom_table);

-- ---------------------------------------------------------------
-- Station avec capacité 0
-- Attendu : refus par station_capacite_check
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO station (
    station_id, nom, commune, capacite,
    latitude, longitude, date_mise_en_service
)
VALUES (
    'S998', 'Station de test', 'Lille', 0,
    50.60000, 3.00000, '2026-10-14'
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Station valide
-- Attendu : S998 avec capacité 15
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO station (
    station_id, nom, commune, capacite,
    latitude, longitude, date_mise_en_service
)
VALUES (
    'S998', 'Station de test', 'Lille', 15,
    50.60000, 3.00000, '2026-10-14'
);

SELECT station_id, capacite
FROM station
WHERE station_id = 'S998';

ROLLBACK;

-- ---------------------------------------------------------------
-- Trajet avec station de départ inexistante
-- Attendu : refus par fk_trajet_station_depart
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO trajet (
    trajet_id, velo_id, depart_horodatage,
    station_depart, station_arrivee,
    duree_secondes, type_usager, usager_ref
)
VALUES (
    'T999999', 'V9999', '2026-10-14 10:00:00',
    'S999', NULL,
    120, 'occasionnel', NULL
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Trajet avec arrivée NULL
-- Attendu : insertion acceptée
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO station (
    station_id, nom, commune, capacite,
    latitude, longitude, date_mise_en_service
)
VALUES (
    'S998', 'Station de test', 'Lille', 15,
    50.60000, 3.00000, '2026-10-14'
);

INSERT INTO trajet (
    trajet_id, velo_id, depart_horodatage,
    station_depart, station_arrivee,
    duree_secondes, type_usager, usager_ref
)
VALUES (
    'T999999', 'V9999', '2026-10-14 10:00:00',
    'S998', NULL,
    120, 'occasionnel', NULL
);

SELECT trajet_id, station_depart, station_arrivee
FROM trajet
WHERE trajet_id = 'T999999';

ROLLBACK;

-- ---------------------------------------------------------------
-- Trajet avec durée 0
-- Attendu : refus par trajet_duree_secondes_check
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO station (
    station_id, nom, commune, capacite,
    latitude, longitude, date_mise_en_service
)
VALUES (
    'S998', 'Station de test', 'Lille', 15,
    50.60000, 3.00000, '2026-10-14'
);

INSERT INTO trajet (
    trajet_id, velo_id, depart_horodatage,
    station_depart, station_arrivee,
    duree_secondes, type_usager, usager_ref
)
VALUES (
    'T999999', 'V9999', '2026-10-14 10:00:00',
    'S998', NULL,
    0, 'occasionnel', NULL
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Incident visant un vélo et une station
-- Attendu : refus par ck_incident_cible
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO station (
    station_id, nom, commune, capacite,
    latitude, longitude, date_mise_en_service
)
VALUES (
    'S998', 'Station de test', 'Lille', 15,
    50.60000, 3.00000, '2026-10-14'
);

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', 'S998', 'vandalisme',
    'ouvert', NULL, NULL
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Incident ouvert valide, sans technicien
-- Attendu : insertion acceptée
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', NULL, 'vandalisme',
    'ouvert', NULL, NULL
);

SELECT incident_id, cible, velo_id, station_id, statut
FROM incident
WHERE incident_id = 'I2026-9999';

ROLLBACK;

-- ---------------------------------------------------------------
-- Résolution antérieure au signalement
-- Attendu : refus par ck_incident_resolution
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', NULL, 'vandalisme',
    'resolu', '2026-10-14 09:00:00', 'Technicien de test'
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Résolution égale au signalement
-- Attendu : insertion acceptée
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', NULL, 'vandalisme',
    'resolu', '2026-10-14 10:00:00', 'Technicien de test'
);

SELECT incident_id, date_signalement, date_resolution
FROM incident
WHERE incident_id = 'I2026-9999';

ROLLBACK;

-- ---------------------------------------------------------------
-- Incident résolu sans date de résolution
-- Attendu : refus par ck_incident_resolution
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', NULL, 'vandalisme',
    'resolu', NULL, 'Technicien de test'
);

ROLLBACK;

-- ---------------------------------------------------------------
-- Incident ouvert avec date de résolution
-- Attendu : refus par ck_incident_resolution
-- ---------------------------------------------------------------

BEGIN;

INSERT INTO incident (
    incident_id, date_signalement, cible,
    velo_id, station_id, type_incident,
    statut, date_resolution, technicien
)
VALUES (
    'I2026-9999', '2026-10-14 10:00:00', 'velo',
    'V9999', NULL, 'vandalisme',
    'ouvert', '2026-10-14 11:00:00', NULL
);

ROLLBACK;