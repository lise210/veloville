"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""

import pytest

from api.services.fiabilisation import normaliser_statut, normaliser_velo_id, convertir_entier_positif, convertir_date, convertir_horodatage, verifier_dates_incident, verifier_cible_incident, verifier_reference_station, normaliser_texte_facultatif, normaliser_texte_obligatoire, normaliser_station_id, normaliser_trajet_id, normaliser_incident_id, normaliser_type_usager, normaliser_usager_ref, verifier_usager_ref
from datetime import date, datetime


###################################################Test sur normaliser_status###############################################################################
def test_statut_deja_valide():
    assert normaliser_statut("ouvert") == "ouvert"

def test_statut_en_majuscules():
    assert normaliser_statut("RESOLU") == "resolu"

def test_statut_avec_espaces():
    assert normaliser_statut(" En cours ") == "en_cours"

def test_statut_inconnu():
    with pytest.raises(ValueError):
        normaliser_statut("inconnu")

def test_statut_absent():
    with pytest.raises(ValueError):
        normaliser_statut(None)



###################################################Test sur normaliser_velo_id###############################################################################
def test_velo_id_deja_valide():
    assert normaliser_velo_id("V1281") == "V1281"

def test_velo_id_en_minuscules():
    assert normaliser_velo_id("v1281") == "V1281"

def test_velo_id_avec_espaces():
    assert normaliser_velo_id(" V1281 ") == "V1281"

def test_velo_id_mauvais_format():
    with pytest.raises(ValueError):
        normaliser_velo_id("V12")

def test_velo_id_absent():
    with pytest.raises(ValueError):
        normaliser_velo_id(None)

###################################################Test sur convertir_entier_positif###############################################################################
def test_entier_positif():
    assert convertir_entier_positif("120") == 120

def test_entier_positif_avec_espaces():
    assert convertir_entier_positif(" 15 ") == 15

def test_entier_zero():
    with pytest.raises(ValueError):
        convertir_entier_positif("0")

def test_entier_negatif():
    with pytest.raises(ValueError):
        convertir_entier_positif("-45")

def test_nombre_decimal():
    with pytest.raises(ValueError):
        convertir_entier_positif("15.5")

def test_entier_non_numerique():
    with pytest.raises(ValueError):
        convertir_entier_positif("quinze")

def test_entier_absent():
    with pytest.raises(ValueError):
        convertir_entier_positif(None)

###################################################Test sur convertir_date###############################################################################
def test_date_valide():
    assert convertir_date("2023-08-07") == date(2023, 8, 7)

def test_date_avec_espaces():
    assert convertir_date(" 2023-08-07 ") == date(2023, 8, 7)

def test_date_impossible():
    with pytest.raises(ValueError):
        convertir_date("2026-02-30")

def test_date_mauvais_format():
    with pytest.raises(ValueError):
        convertir_date("07/08/2023")

def test_date_absente():
    with pytest.raises(ValueError):
        convertir_date(None)

def test_date_vide():
    with pytest.raises(ValueError):
        convertir_date("")

###################################################Test sur convertir_horodatage###############################################################################
def test_horodatage_avec_secondes():
    resultat = convertir_horodatage("2026-08-24 08:39:56")
    assert resultat == datetime(2026, 8, 24, 8, 39, 56)

def test_horodatage_sans_secondes():
    resultat = convertir_horodatage("2026-07-23 18:00")
    assert resultat == datetime(2026, 7, 23, 18, 0, 0)

def test_horodatage_format_francais():
    resultat = convertir_horodatage("24/08/2026 11:01")
    assert resultat == datetime(2026, 8, 24, 11, 1, 0)

def test_horodatage_avec_espaces():
    resultat = convertir_horodatage(" 2026-07-23 18:00 ")
    assert resultat == datetime(2026, 7, 23, 18, 0, 0)

def test_horodatage_date_impossible():
    with pytest.raises(ValueError):
        convertir_horodatage("2026-02-30 10:00")

def test_horodatage_heure_impossible():
    with pytest.raises(ValueError):
        convertir_horodatage("2026-07-23 25:00")

def test_horodatage_format_inconnu():
    with pytest.raises(ValueError):
        convertir_horodatage("23 juillet 2026 à 18h")

def test_horodatage_absent():
    with pytest.raises(ValueError):
        convertir_horodatage(None)

def test_horodatage_vide():
    with pytest.raises(ValueError):
        convertir_horodatage("")

###################################################Test sur verifier_dates_incident###############################################################################
def test_incident_resolu_dates_valides():
    verifier_dates_incident(
        "resolu",
        datetime(2026, 10, 14, 10, 0),
        datetime(2026, 10, 14, 11, 0))

def test_incident_resolu_dates_egales():
    verifier_dates_incident(
        "resolu",
        datetime(2026, 10, 14, 10, 0),
        datetime(2026, 10, 14, 10, 0))

def test_incident_ouvert_sans_resolution():
    verifier_dates_incident(
        "ouvert",
        datetime(2026, 10, 14, 10, 0),
        None)

def test_incident_en_cours_sans_resolution():
    verifier_dates_incident(
        "en_cours",
        datetime(2026, 10, 14, 10, 0),
        None)

def test_incident_resolu_sans_resolution():
    with pytest.raises(ValueError):
        verifier_dates_incident(
            "resolu",
            datetime(2026, 10, 14, 10, 0),
            None)

def test_incident_resolution_avant_signalement():
    with pytest.raises(ValueError):
        verifier_dates_incident(
            "resolu",
            datetime(2026, 10, 14, 10, 0),
            datetime(2026, 10, 14, 9, 0))

def test_incident_ouvert_avec_resolution():
    with pytest.raises(ValueError):
        verifier_dates_incident(
            "ouvert",
            datetime(2026, 10, 14, 10, 0),
            datetime(2026, 10, 14, 11, 0))

def test_incident_en_cours_avec_resolution():
    with pytest.raises(ValueError):
        verifier_dates_incident(
            "en_cours",
            datetime(2026, 10, 14, 10, 0),
            datetime(2026, 10, 14, 11, 0))

###################################################Test sur verifier_cible_incident###############################################################################
def test_cible_velo_valide():
    verifier_cible_incident("velo", "V1281", None)

def test_cible_station_valide():
    verifier_cible_incident("station", None, "S001")

def test_cible_velo_sans_velo():
    with pytest.raises(ValueError):
        verifier_cible_incident("velo", None, None)

def test_cible_station_sans_station():
    with pytest.raises(ValueError):
        verifier_cible_incident("station", None, None)

def test_cible_velo_avec_deux_references():
    with pytest.raises(ValueError):
        verifier_cible_incident("velo", "V1281", "S001")

def test_cible_station_avec_deux_references():
    with pytest.raises(ValueError):
        verifier_cible_incident("station", "V1281", "S001")

def test_cible_velo_avec_reference_station():
    with pytest.raises(ValueError):
        verifier_cible_incident("velo", None, "S001")

def test_cible_station_avec_reference_velo():
    with pytest.raises(ValueError):
        verifier_cible_incident("station", "V1281", None)

def test_cible_inconnue():
    with pytest.raises(ValueError):
        verifier_cible_incident("autre", "V1281", None)

###################################################Test sur verifier_reference_station###############################################################################
def test_reference_station_connue():
    verifier_reference_station("S001", ["S001", "S002"])

def test_reference_station_inconnue():
    with pytest.raises(ValueError):
        verifier_reference_station("S999", ["S001", "S002"])

def test_reference_station_absente():
    with pytest.raises(ValueError):
        verifier_reference_station(None, ["S001", "S002"])

def test_reference_station_referentiel_vide():
    with pytest.raises(ValueError):
        verifier_reference_station("S001", [])

###################################################Test sur normaliser_texte_facultatif###############################################################################
def test_texte_facultatif_present():
    assert normaliser_texte_facultatif("S001") == "S001"

def test_texte_facultatif_avec_espaces():
    assert normaliser_texte_facultatif(" S001 ") == "S001"

def test_texte_facultatif_absent():
    assert normaliser_texte_facultatif(None) is None

def test_texte_facultatif_vide():
    assert normaliser_texte_facultatif("") is None

def test_texte_facultatif_uniquement_espaces():
    assert normaliser_texte_facultatif("   ") is None

###################################################Test sur normaliser_texte_obligatoire###############################################################################
def test_texte_obligatoire_valide():
    assert normaliser_texte_obligatoire("Lille", 100) == "Lille"

def test_texte_obligatoire_avec_espaces():
    assert normaliser_texte_obligatoire(" Lille ", 100) == "Lille"

def test_texte_obligatoire_longueur_limite():
    assert normaliser_texte_obligatoire("Lille", 5) == "Lille"

def test_texte_obligatoire_trop_long():
    with pytest.raises(ValueError):
        normaliser_texte_obligatoire("Lille", 4)

def test_texte_obligatoire_absent():
    with pytest.raises(ValueError):
        normaliser_texte_obligatoire(None, 100)

def test_texte_obligatoire_vide():
    with pytest.raises(ValueError):
        normaliser_texte_obligatoire("", 100)

def test_texte_obligatoire_uniquement_espaces():
    with pytest.raises(ValueError):
        normaliser_texte_obligatoire("   ", 100)

###################################################Test sur normaliser_station_id###############################################################################
def test_station_id_valide():
    assert normaliser_station_id("S001") == "S001"

def test_station_id_minuscules():
    assert normaliser_station_id("s001") == "S001"

def test_station_id_avec_espaces():
    assert normaliser_station_id(" S001 ") == "S001"

def test_station_id_mauvais_format():
    with pytest.raises(ValueError):
        normaliser_station_id("S01")

def test_station_id_trop_de_chiffres():
    with pytest.raises(ValueError):
        normaliser_station_id("S0001")

def test_station_id_absent():
    with pytest.raises(ValueError):
        normaliser_station_id(None)

def test_station_id_vide():
    with pytest.raises(ValueError):
        normaliser_station_id("")

###################################################Test sur normaliser_trajet_id###############################################################################
def test_trajet_id_valide():
    assert normaliser_trajet_id("T480001") == "T480001"

def test_trajet_id_minuscules():
    assert normaliser_trajet_id("t480001") == "T480001"

def test_trajet_id_avec_espaces():
    assert normaliser_trajet_id(" T480001 ") == "T480001"

def test_trajet_id_mauvais_format():
    with pytest.raises(ValueError):
        normaliser_trajet_id("T48001")

def test_trajet_id_trop_de_chiffres():
    with pytest.raises(ValueError):
        normaliser_trajet_id("T4800001")

def test_trajet_id_absent():
    with pytest.raises(ValueError):
        normaliser_trajet_id(None)

def test_trajet_id_vide():
    with pytest.raises(ValueError):
        normaliser_trajet_id("")

###################################################Test sur normaliser_incident_id###############################################################################
def test_incident_id_valide():
    assert normaliser_incident_id("I2026-0001") == "I2026-0001"

def test_incident_id_minuscules():
    assert normaliser_incident_id("i2026-0001") == "I2026-0001"

def test_incident_id_avec_espaces():
    assert normaliser_incident_id(" I2026-0001 ") == "I2026-0001"

def test_incident_id_mauvais_format():
    with pytest.raises(ValueError):
        normaliser_incident_id("I2026-001")

def test_incident_id_trop_de_chiffres():
    with pytest.raises(ValueError):
        normaliser_incident_id("I2026-00001")

def test_incident_id_absent():
    with pytest.raises(ValueError):
        normaliser_incident_id(None)

def test_incident_id_vide():
    with pytest.raises(ValueError):
        normaliser_incident_id("")

###################################################Test sur normaliser_type_usager###############################################################################
def test_type_usager_abonne():
    assert normaliser_type_usager("abonne") == "abonne"

def test_type_usager_occasionnel():
    assert normaliser_type_usager("occasionnel") == "occasionnel"

def test_type_usager_majuscules_et_espaces():
    assert normaliser_type_usager(" ABONNE ") == "abonne"

def test_type_usager_inconnu():
    with pytest.raises(ValueError):
        normaliser_type_usager("autre")

def test_type_usager_absent():
    with pytest.raises(ValueError):
        normaliser_type_usager(None)

def test_type_usager_vide():
    with pytest.raises(ValueError):
        normaliser_type_usager("")

###################################################Test sur normaliser_usager_ref###############################################################################
def test_usager_ref_valide():
    assert normaliser_usager_ref("Ued311b7d") == "Ued311b7d"

def test_usager_ref_avec_espaces():
    assert normaliser_usager_ref(" Ued311b7d ") == "Ued311b7d"

def test_usager_ref_absente():
    assert normaliser_usager_ref(None) is None

def test_usager_ref_vide():
    assert normaliser_usager_ref("") is None

def test_usager_ref_mauvaise_longueur():
    with pytest.raises(ValueError):
        normaliser_usager_ref("U123")

def test_usager_ref_caractere_non_hexadecimal():
    with pytest.raises(ValueError):
        normaliser_usager_ref("U1234567G")

###################################################Test sur verifier_usager_ref###############################################################################
def test_abonne_avec_pseudonyme():
    assert verifier_usager_ref("abonne", "Ued311b7d") is None

def test_occasionnel_sans_pseudonyme():
    assert verifier_usager_ref("occasionnel", None) is None

def test_abonne_sans_pseudonyme():
    assert verifier_usager_ref("abonne", None) == ("Pseudonyme absent pour un abonné")

def test_occasionnel_avec_pseudonyme():
    with pytest.raises(ValueError):
        verifier_usager_ref("occasionnel", "Ued311b7d")

def test_pseudonyme_type_usager_inconnu():
    with pytest.raises(ValueError):
        verifier_usager_ref("autre", None)

###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################


###################################################Test sur normaliser_status###############################################################################
