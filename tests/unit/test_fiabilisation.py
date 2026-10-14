"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""

import pytest

from api.services.fiabilisation import normaliser_statut, normaliser_velo_id, convertir_entier_positif


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

###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################
