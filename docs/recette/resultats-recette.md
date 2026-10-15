# Résultats de recette — VéloVille V1

## Relevé d’exécution

| Cas | Date | Version testée (commit ou tag) | Statut | Preuve | Anomalie |
|---|---|---|---|---|---|
| REC-01 | 13/10/2026 | Développement de l’import, avant livraison v0.0.3, commit exact non relevé | OK | Deux imports successifs : 120 stations, 2 002 trajets et 177 incidents après chaque exécution. | Aucune constatée |
| REC-02 | 14/10/2026 | Développement de l’import, avant livraison v0.0.3, commit exact non relevé | OK | Journal docs/journal_import.csv et comptages : 120 stations, 2 002 trajets, 177 incidents. 19 rejets, 12 doublons, aucune station d’arrivée inconnue. | Aucune constatée |
| REC-03 | 13/10/2026 | 145305e | OK | Connexions vérifiées dans Swagger avec exploitant01 et direction01 : réponse 200, jeton non vide et rôle correspondant. | Aucune constatée |
| REC-04 | 13/10/2026 | 145305e | OK | Swagger : mauvais mot de passe et compte inconnu refusés avec 401 et le même message "Identifiants invalides". | Aucune constatée |
| REC-05 | 15/10/2026 | 97da69b | OK | Test sur Swagger : /stations sans jeton --> 401, jeton invalide --> 401, /sante sans jeton --> 200. | Aucune constatée |
| REC-06 | 15/10/2026 | 97da69b | KO | Swagger 403, 200 et 422. Contrôles SQL avant/après. état initial restauré. | ANO-001 : message 403 différent du texte attendu |
| REC-07 | 15/10/2026 | 97da69b | OK | Swagger : pagination, filtre Lille et refus des paramètres hors limites. | Aucune constatée |
| REC-08 | 15/10/2026 | 97da69b | KO | Swagger : S001 --> 200, S999 --> 404 avec "Station inconnue". | ANO-002 : message 404 différent du texte attendu |
| REC-09 | 15/10/2026 | 97da69b | OK | Swagger comparée au SQL. Total GET /trajets égal à 2 002. | Aucune constatée |
| REC-10 | 15/10/2026 | 97da69b | OK | Streamlit : résultat vide, erreurs API sur Stations et Indicateurs, puis retour du tableau après redémarrage de uvicorn. | Aucune constatée |

## Résultats obtenus

### REC-01 — Import idempotent

Les deux exécutions se sont terminées sans erreur.

| Table | Premier import | Second import |
|---|---:|---:|
| station | 120 | 120 |
| trajet | 2 002 | 2 002 |
| incident | 177 | 177 |

Les comptages sont identiques après les deux exécutions.

### REC-02 — Rejets journalisés et cohérence des volumes

| Fichier | Lignes CSV | Importées | Rejetées | Doublons écartés |
|---|---:|---:|---:|---:|
| stations.csv | 120 | 120 | 0 | 0 |
| trajets.csv | 2 030 | 2 002 | 16 | 12 |
| incidents.csv | 180 | 177 | 3 | 0 |

Pour chaque fichier, importées + rejetées + doublons écartés
correspond au nombre de lignes du CSV.

Le journal contient les six informations demandées :
fichier_source, identifiant, colonne, valeur, motif et decision.

Les 136 normalisations et 25 avertissements ne sont pas des rejets.

La requête recherchant les stations d’arrivée renseignées mais
inexistantes a renvoyé 0.

### REC-03 — Connexion acceptée

Les appels POST /auth/login ont été effectués dans Swagger
avec les deux comptes fournis.

| Compte | Code HTTP | access_token | token_type | role |
|---|---:|---|---|---|
| exploitant01 | 200 | Non vide | bearer | exploitant |
| direction01 | 200 | Non vide | bearer | direction |

Les réponses contiennent les informations attendues.

### REC-04 — Connexion refusée

Deux appels POST /auth/login ont été vérifiés dans Swagger :

| Cas | Code HTTP | Message obtenu |
|---|---:|---|
| exploitant01 avec un mauvais mot de passe | 401 | Identifiants invalides |
| Compte inconnu | 401 | Identifiants invalides |

Le corps de réponse est identique dans les deux cas :

`{"detail": "Identifiants invalides"}`

Le message ne permet pas de distinguer un compte inconnu
d’un mot de passe incorrect.

### REC-05 — Route protégée sans jeton

| Appel | Code HTTP | Corps obtenu |
|---|---:|---|
| GET /stations sans jeton | 401 | `{"detail": "Authentification requise"}` |
| GET /stations avec jeton.invalide.xyz | 401 | `{"detail": "Token invalide"}` |
| GET /sante sans jeton | 200 | `{"statut": "ok"}` |

Les trois réponses correspondent au résultat attendu.

### REC-06 — Rôle direction refusé sur la modification d’un incident

Incident utilisé : I2026-0065, initialement ouvert, sans date de résolution.

| Étape | Résultat obtenu |
|---|---|
| Modification avec direction01 | 403, message "Rôle non autorisé pour cette action" |
| Vérification en base après refus | Statut `ouvert`, inchangé |
| Modification avec exploitant01 | 200, statut `en_cours` |
| Vérification en base après modification | Statut `en_cours` |
| Seconde demande en_cours avec exploitant01 | 422, message "Transition de statut non autorisee" |

Le contrôle des droits et des transitions fonctionne.
Le message 403 diffère du texte attendu : "Acces reserve au role exploitant"

Après le test, l’incident a été restauré au statut ouvert avec une date de résolution NULL.

### REC-07 — Pagination

Vérifications effectuées avec le compte direction01.

| Appel GET /stations | Résultat obtenu |
|---|---|
| page=1, taille_page=50 | 200, total 120, page 1, taille 50, 50 résultats, premier identifiant S001 |
| page=3, taille_page=50 | 200, total 120, 20 résultats |
| commune=Lille, page=1, taille_page=100 | 200, total 46, 46 résultats, commune Lille uniquement |
| page=0 | 422, erreur sur la valeur minimale de page |
| `taille_page`=101 | 422, erreur sur la valeur maximale de `taille_page` |

Les résultats correspondent aux attentes du plan.

### REC-08 — Station introuvable

Vérifications effectuées avec le compte direction01.

| Appel | Résultat attendu | Résultat obtenu |
|---|---|---|
| GET /stations/S001 | 200, S001, Lille - Gare | Conforme |
| GET /stations/S999 | 404, `{"detail": "Station introuvable"}` | 404, `{"detail": "Station inconnue"}` |

La station existante est correctement renvoyée et la station inexistante produit bien un code 404. Le message ne correspond toutefois pas au texte exact attendu dans le plan.

### REC-09 — Cohérence de l’indicateur "activité par jour"

Période vérifiée : du 24/08/2026 au 30/08/2026 inclus.
Compte utilisé : direction01.

| Jour | Comptage SQL | Indicateur API |
|---|---:|---:|
| 2026-08-24 | 329 | 329 |
| 2026-08-25 | 311 | 311 |
| 2026-08-26 | 306 | 306 |
| 2026-08-27 | 300 | 300 |
| 2026-08-28 | 315 | 315 |
| 2026-08-29 | 219 | 219 |
| 2026-08-30 | 222 | 222 |
| Total | 2 002 | 2 002 |

Les jours, les comptages et leur ordre sont identiques.

GET /trajets sur la même période renvoie total = 2002, égal à la somme des `nb_trajets` de l’indicateur.

### REC-10 — Front : état vide et état d’erreur

Compte utilisé : direction01.

| Étape | Résultat obtenu |
|---|---|
| Stations, page 100 | Message "Aucun résultat pour ces critères." |
| API arrêtée, rechargement de Stations | Message "Impossible de joindre l’API" |
| API arrêtée, actualisation des Indicateurs | Message "Impossible de joindre l’API" |
| API redémarrée, Stations page 1 | Tableau affiché à nouveau : 120 stations au total |

Aucune trace Python ni code source n’a été affiché lors des erreurs.

## Synthèse initiale

10 cas renseignés : 8 OK, 2 KO, 0 NT.
Les cas REC-01 à REC-04 reprennent des essais antérieurs : leurs dates et versions restent à préciser.

Deux anomalies ouvertes :
- ANO-001 : message 403 différent du texte attendu dans REC-06.
- ANO-002 : message 404 différent du texte attendu dans REC-08.

Aucune anomalie corrigée pour le moment.

## Rejeux après corrections

| Cas | Date et heure | Version | Résultat | Anomalie |
|---|---|---|---|---|
| REC-08 | 15/10/2026, 10h20 | babea35 | OK : S001 --> 200, S999 --> 404 avec "Station introuvable" | ANO-002 fermée |
| REC-06 | 15/10/2026, 10h30| babea35 | OK : 403 conforme, modification 200, seconde demande 422, état initial restauré | ANO-001 fermée |

## Synthèse après corrections

Résultats consolidés des dix cas : 10 OK, 0 KO, 0 NT.
Les essais antérieurs restent identifiés dans le relevé initial.

Deux anomalies corrigées et rejouées avec succès :
- ANO-001 : fermée après rejeu de REC-06.
- ANO-002 : fermée après rejeu de REC-08.

## Axes d’amélioration

- Utiliser une base dédiée aux tests pour éviter de modifier les données utilisées par l’application.
- Conserver dès chaque essai la date, la version testée et les fichiers de preuve pour faciliter le suivi.
- Réinitialiser automatiquement la pagination lors d’un changement de filtre, afin d’éviter de rester sur une page sans résultat.
- Compléter le script de sauvegarde demandé. La sauvegarde et la restauration n’ont pas été vérifiées. N'a pas été vu en formation, cette partie reste à réaliser avant l'oral final (je me renseignerai sur le sujet).


## Procès-verbal de recette — VéloVille V1

### 1. Identification

Application : VéloVille.
Version initiale de la campagne : 97da69b.
Version des corrections et des rejeux : babea35.
Date de clôture des rejeux : 15/10/2026.

Environnement : Windows, Python 3.14.7, PostgreSQL 18,
API FastAPI et interface Streamlit exécutées localement.

Exécution des vérifications : Lise, développeuse.
Comptes utilisés : exploitant01 et direction01.

### 2. Périmètre recetté

Cas REC-01 à REC-10 du plan fourni.

Les cas REC-06 et REC-08 ont été rejoués après correction.

### 3. Résultats

Relevé initial : 8 OK, 2 KO, 0 NT.

Résultats consolidés après corrections : 10 OK, 0 KO, 0 NT.

Deux anomalies mineures relevées :
- ANO-001 : message 403, corrigée et fermée.
- ANO-002 : message 404, corrigée et fermée.

Vérification automatisée : 170 tests réussis.
Couverture des services : 95 %.

### 4. Réserves bloquantes

Aucune anomalie bloquante constatée dans les cas exécutés.

### 5. Réserves non bloquantes

Références des preuves et versions exactes lorsqu’elles sont disponibles.

### 6. Décision proposée

Les dix cas sont déclarés conformes après les corrections.
La réserve porte sur les preuves (oublie de garder des captures d'écran).


### 7. Validation

Développeuse : Lise - 15/10/2026.
Commanditaire : validation non recueillie.