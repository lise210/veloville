"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""

import pytest

from api.services.fiabilisation import normaliser_statut

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



###################################################Test sur normaliser_status###############################################################################


###################################################Test sur normaliser_status###############################################################################


###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################



###################################################Test sur normaliser_status###############################################################################
