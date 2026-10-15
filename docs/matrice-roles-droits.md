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

## Données sensibles

- **Mots de passe** : les comptes sont stockés avec un hachage bcrypt
  dans PostgreSQL. Le formulaire de connexion masque la saisie.
  Les mots de passe ne sont pas écrits dans les journaux.

- **Jeton JWT** : il est signé avec le secret `JWT_SECRET` et possède une date d'expiration. L'API refuse les jetons invalides ou expirés.
  Dans Streamlit, il est conservé dans `st.session_state` et transmis dans l'en-tête Authorization. Il n'est affiché ni dans l'interface ni dans l'URL. La déconnexion le retire de la session.

- **Référence usager** : `usager_ref` est un identifiant pseudonymisé.
  Les trajets qui le contiennent sont accessibles uniquement aux utilisateurs authentifiés.

- **Configuration** : le secret JWT et les paramètres de connexion sont lus dans l'environnement. Le fichier .env reste local et est ignoré par Git. Le fichier .env.example ne contient pas de secret réel.

- **Droits d'accès** : les contrôles sont réalisés par l'API.
  Seul l'exploitant peut modifier le statut d'un incident.
  Le rôle direction dispose d'un accès en lecture.