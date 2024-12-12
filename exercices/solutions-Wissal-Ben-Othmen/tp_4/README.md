# Résumé du Travail - TP 4 : Ingestion de Données et Recherche Vectorielle

## Réalisations Principales

J'ai avec succès terminé et déployé ce projet TP4 sur Google Cloud Platform (GCP), qui impliquait plusieurs étapes clés :

1. **Ingestion et Traitement de Données**
   - Développé des scripts Python pour automatiser le téléchargement et l'ingestion de fichiers depuis Google Cloud Storage
   - Utilisé VertexAI pour générer des embeddings vectoriels
   - Créé un index de recherche vectorielle FAISS pour une récupération efficace des documents

2. **Développement d'API et Application**
   - Implémenté une API FastAPI pour la recherche de documents
   - Développé une application Streamlit interactive
   - Intégré Google Generative AI pour le traitement des requêtes
   - Supporté des requêtes multilingues (Anglais, Français, Arabe)

3. **Déploiement Cloud**
   - Déployé avec succès l'API et l'application sur Google Cloud Run
   - Liens de déploiement :
     * API : [https://wissal-api-1021317796643.europe-west1.run.app/](https://wissal-api-1021317796643.europe-west1.run.app/)
     * Application Streamlit : [https://wissalbenothmen-tp4-streamlit-1021317796643.europe-west1.run.app/](https://wissalbenothmen-tp4-streamlit-1021317796643.europe-west1.run.app/)
   - Configuré des conteneurs Docker pour l'API et l'application Streamlit

4. **Bonnes Pratiques de Développement**
   - Appliqué rigoureusement les normes de qualité de code avec `pylint` et `flake8`
   - Capturé et validé les résultats des vérifications de code qualité

## Captures d'Écran de Validation

### Vérification de Qualité de Code
![Pylint et Flake8 - Capture 1](Tp4_pylint_flake8(1).png)
![Pylint et Flake8 - Capture 2](Tp4_pylint_flake8(2).png)

### Captures d'Écran de l'Application

#### Capture d'écran de la page d'accueil
![Capture d'écran de la page d'accueil](capture_page_accueil.png)

#### Capture d'écran de recherche de documents
![Capture d'écran de recherche de documents](capture_recherche_documents.png)

#### Capture d'écran de résultats de requête
![Capture d'écran de résultats de requête](capture_resultats_requete.png)

## Conclusion

Le projet a été déployé avec succès sur GCP, démontrant une approche complète de l'ingestion, du traitement et de la recherche de documents vectoriels, tout en respectant les meilleures pratiques de développement logiciel.
