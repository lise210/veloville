"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""

import pytest

from api.services.fiabilisation import normaliser_statut, normaliser_velo_id, convertir_entier_positif, convertir_date, convertir_horodatage
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

###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################
