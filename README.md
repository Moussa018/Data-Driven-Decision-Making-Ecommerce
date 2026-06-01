# Data-Driven Decision Making : Système Prédictif du Churn E-Commerce

Ce projet a été développé dans le cadre du module **Data-Driven Decision Making**. Il implémente l'intégralité d'un pipeline décisionnel basé sur la donnée, depuis le cadrage métier jusqu'à la mesure d'impact, en passant par le déploiement d'un système d'aide à la décision interactif pour optimiser la rétention client (Churn) à 30 jours.

---

##  Schéma d'Architecture du Pipeline

Le système s'articule autour d'une architecture modulaire qui transforme les données transactionnelles et d'expérience brute en indicateurs stratégiques et prédictions actionnables :


```

```
              ┌─────────────────────────────────────┐
              │        SOURCES DE DONNÉES           │
              │  (Transactions Olist + Avis Client) │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │   INGESTION & NETTOYAGE (Colab)     │
              │   (Fusion Left Join, Imputation MD) │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │      FEATURE ENGINEERING & ML       │
              │   (Scikit-Learn, XGBoost, SHAP)     │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │      COUCHE DE VISUALISATION        │
              │        (Dashboard Streamlit)        │
              └──────────┬─────────────────────┬────┘
                         │                     │
                         ▼                     ▼
              ┌──────────────────┐   ┌──────────────────┐
              │ VUES DÉCISIONNEL │   │ SIMULATEUR       │
              │ (Dir/Mkt/Ops/Tech)│   │ PREDICTIF (ML)   │
              └──────────────────┘   └──────────────────┘

```

```

---

##  Description des Fichiers du Dépôt

* **`notebook_analyse_decisionnelle.ipynb`** : Le Notebook Jupyter principal (développé sur Google Colab). Il contient l'audit des données, l'analyse statistique exploratoire (EDA), les tests d'hypothèses ($t\text{-test}$), le clustering $K\text{-Means}$ et l'entraînement comparatif des 3 modèles de Machine Learning.
* **`app.py`** : Le code source Python de l'application interactive **Streamlit** matérialisant le dashboard d'aide à la décision avec ses 5 vues spécifiques.
* **`requirements.txt`** : La liste des dépendances et bibliothèques Python nécessaires avec leurs versions pour garantir la reproductibilité complète du projet.
* **`A_B_Testing_Plan.md`** : Document protocolaire détaillant le plan d'expérimentation mathématique pour valider l'impact financier des recommandations.

---

## ⚙️ Instructions d'Installation et Lancement

Suivez ces étapes pour installer et exécuter le projet localement sur votre machine :

### 1. Prérequis
Assurez-vous d'avoir **Python 3.9+** et **Git** installés sur votre système.

### 2. Cloner le dépôt et se positionner
Ouvrez votre terminal et exécutez les commandes suivantes :
```bash
git clone https://github.com/Moussa018/Data-Driven-Decision-Making-Ecommerce.git

```

### 3. Créer un environnement virtuel (Recommandé)

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Installer les dépendances obligatoires

```bash
pip install -r requirements.txt

```

### 5. Lancer le Dashboard Decisionnel Streamlit

```bash
streamlit run app.py

```

Une fois la commande exécutée, votre navigateur internet s'ouvrira automatiquement à l'adresse locale : `http://localhost:8501`.

---

## Aperçu des 5 Vues du Dashboard

L'interface Streamlit propose un basculement dynamique selon le profil utilisateur :

1. **Vue Direction (Stratégique)** : Suivi du Chiffre d'Affaires global, du taux de Churn macro et du ROI simulé.
2. **Vue Marketing (Segmentation)** : Analyse descriptive des groupes de clients issus du clustering pour affiner le ciblage.
3. **Vue Opérations (Liste d'Alerte)** : Liste chirurgicale des clients à haut risque identifiés par XGBoost pour des actions de phoning prioritaires.
4. **Vue Technique (SHAP Importance)** : Transparence totale des features décisionnelles globales issues des valeurs SHAP.
5. **Simulateur de Churn en Direct** : Outil interactif permettant d'ajuster les métriques d'un client pour prédire son score d'attrition en temps réel.

```



```
