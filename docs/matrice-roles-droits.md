# Matrice rôles × droits

Les rôles exploitant et direction doivent utiliser un JWT valide
pour accéder aux routes protégées.

| Méthode et route | Anonyme | Exploitant | Direction |
|---|---|---|---|
| GET /sante | Autorisé | Autorisé | Autorisé |
| POST /auth/login | Autorisé | Autorisé | Autorisé |
| GET /stations | Refusé : 401 | Autorisé | Autorisé |
| GET /stations/{station_id} | Refusé : 401 | Autorisé | Autorisé |
| GET /trajets | Refusé : 401 | Autorisé | Autorisé |
| GET /incidents | Refusé : 401 | Autorisé | Autorisé |
| PUT /incidents/{incident_id}/statut | Refusé : 401 | Autorisé | Refusé : 403 |
| GET /indicateurs/activite-par-jour | Refusé : 401 | Autorisé | Autorisé |
| GET /indicateurs/stations-actives | Refusé : 401 | Autorisé | Autorisé |
| GET /indicateurs/incidents-par-statut | Refusé : 401 | Autorisé | Autorisé |

## Codes de refus

- 401 : authentification absente, jeton invalide ou expiré.
- 403 : utilisateur connecté, mais rôle non autorisé.
