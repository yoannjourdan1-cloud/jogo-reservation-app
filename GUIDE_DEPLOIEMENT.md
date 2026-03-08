# Guide de Déploiement : Votre Application de Réservation CHEZ JOGO

Félicitations ! Votre application est prête. Ce guide vous explique comment la déployer **gratuitement** et la rendre accessible à vos invités via une URL publique protégée par mot de passe. Vous pourrez ainsi continuer à l'utiliser indéfiniment, même après votre période d'essai Manus.

L'opération complète prend environ **10 minutes** et ne requiert aucune compétence technique avancée. Suivez simplement ces 3 grandes étapes.

---

## Étape 1 : Déployer le Script d'Écriture sur Google (3 minutes)

Pour que l'application puisse écrire les réservations dans votre Google Sheet, nous allons déployer un petit script (que j'ai déjà écrit pour vous) directement dans votre compte Google. Ce script agira comme un pont sécurisé entre l'application et votre fichier.

1.  **Ouvrez Google Apps Script** : [script.google.com/home/my](https://script.google.com/home/my)
2.  Cliquez sur **"Nouveau projet"** en haut à gauche.
3.  **Nommez le projet** : en haut, remplacez "Projet sans titre" par `Script JOGO`.
4.  **Collez le code du script** :
    *   Supprimez tout le code existant dans l'éditeur (`function myFunction() { ... }`).
    *   Copiez l'intégralité du code contenu dans le fichier `apps_script.gs` (fourni avec ce guide) et collez-le dans l'éditeur.
5.  **Déployez le script en tant qu'application web** :
    *   Cliquez sur le bouton bleu **"Déployer"** en haut à droite, puis **"Nouveau déploiement"**.
    *   Cliquez sur l'icône d'engrenage ("Sélectionner le type") et choisissez **"Application Web"**.
    *   Dans la nouvelle fenêtre, configurez comme suit :
        *   **Description** : `API Réservation JOGO`
        *   **Exécuter en tant que** : `Moi (votre.email@gmail.com)`
        *   **Qui a accès** : **`Tout le monde`** (c'est crucial pour que Streamlit puisse l'appeler).
    *   Cliquez sur **"Déployer"**.
6.  **Autorisez le script** :
    *   Google va vous demander une autorisation. Cliquez sur **"Autoriser l'accès"**.
    *   Choisissez votre compte Google.
    *   Un avertissement "Google n'a pas validé cette application" peut apparaître. C'est normal. Cliquez sur **"Paramètres avancés"** puis sur **"Accéder à Script JOGO (non sécurisé)"**.
    *   Cliquez sur **"Autoriser"** sur la dernière page.
7.  **Copiez l'URL de l'application web** :
    *   Une fois le déploiement terminé, une fenêtre apparaît avec une **URL d'application web**. Elle se termine par `/exec`.
    *   **Copiez cette URL et conservez-la précieusement.** Nous en aurons besoin dans la dernière étape.

> **Bravo !** Le pont entre votre application et votre Google Sheet est maintenant en place.

---

## Étape 2 : Mettre le Code de l'Application sur GitHub (5 minutes)

Streamlit Community Cloud, le service d'hébergement gratuit que nous allons utiliser, fonctionne en se connectant à un dépôt (repository) GitHub.

1.  **Créez un compte GitHub** : si vous n'en avez pas, créez-en un gratuitement sur [github.com](https://github.com).
2.  **Créez un nouveau dépôt** :
    *   Une fois connecté, cliquez sur le `+` en haut à droite, puis **"New repository"**.
    *   **Nom du dépôt** : `jogo-reservation-app` (ou un nom de votre choix).
    *   **Description** : `Application de réservation pour l'événement CHEZ JOGO.`
    *   Sélectionnez **"Public"**.
    *   **NE cochez PAS** "Add a README file".
    *   Cliquez sur **"Create repository"**.
3.  **Uploadez les fichiers de l'application** :
    *   Sur la page de votre nouveau dépôt, cliquez sur le lien **"uploading an existing file"**.
    *   Faites glisser et déposez **tous les fichiers** que je vous ai fournis dans le dossier `jogo_reservation` :
        *   `app.py`
        *   `requirements.txt`
        *   `.gitignore`
        *   Le dossier `.streamlit` avec son fichier `secrets.toml` dedans.
    *   Une fois les fichiers uploadés, cliquez sur **"Commit changes"**.

> **Parfait !** Le code de votre application est maintenant prêt à être déployé.

---

## Étape 3 : Déployer l'Application sur Streamlit Community Cloud (2 minutes)

C'est la dernière ligne droite !

1.  **Connectez-vous à Streamlit Community Cloud** : [share.streamlit.io/signup](https://share.streamlit.io/signup)
    *   Inscrivez-vous en utilisant votre compte GitHub. C'est plus simple et plus rapide.
2.  **Déployez votre application** :
    *   Une fois sur votre tableau de bord, cliquez sur **"New app"**.
    *   **Repository** : Choisissez le dépôt `jogo-reservation-app` que vous venez de créer.
    *   **Branch** : `main` (ou `master`).
    *   **Main file path** : `app.py` (Streamlit le détecte généralement tout seul).
    *   **App URL** : Personnalisez le nom si vous le souhaitez (ex: `jogo-2026`).
3.  **Ajoutez le Secret (l'URL du script)** :
    *   Avant de cliquer sur "Deploy!", cliquez sur **"Advanced settings..."**.
    *   Dans la section **"Secrets"**, collez le texte suivant :
        ```toml
        APPS_SCRIPT_URL = "VOTRE_URL_COPIEE_A_L_ETAPE_1"
        ```
    *   **Remplacez `VOTRE_URL_COPIEE_A_L_ETAPE_1`** par l'URL de l'application web que vous avez copiée à la fin de l'étape 1.
    *   Cliquez sur **"Save"**.
4.  **Lancez le déploiement** :
    *   Cliquez sur le bouton **"Deploy!"**.

Streamlit va maintenant construire et déployer votre application. Cela peut prendre une ou deux minutes. Vous verrez une animation de cuisson de gâteau pendant le processus. 🎂

Une fois terminé, votre application sera **en ligne, fonctionnelle et accessible** à l'URL que vous avez définie !

---

### Et voilà !

Vous pouvez maintenant partager le lien de votre application (et le mot de passe `JOGO2026`) avec vos invités. Chaque réservation mettra à jour votre Google Sheet en temps réel.

N'hésitez pas si vous avez la moindre question lors du déploiement !
