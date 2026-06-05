# Data-Driven Decision Making : Système Prédictif du Risque d'Insatisfaction E-Commerce

Ce projet a été développé dans le cadre du module **Data-Driven Decision Making**. Il implémente l'intégralité d'un pipeline décisionnel basé sur la donnée, depuis le cadrage métier jusqu'à la mesure d'impact, en passant par le déploiement d'un système d'aide à la décision interactif.

> **Note méthodologique.** Le dataset Olist est composé à ~97 % d'acheteurs uniques : une cible de *ré-achat* (« churn » littéral) y est statistiquement dégénérée (> 99 % d'une seule classe) et favorise les fuites de données. Nous modélisons donc le **risque d'expérience client négative** (note ≤ 2/5), déterminant avancé et actionnable de l'attrition. Toutes les variables explicatives sont **connues avant la rédaction de l'avis** (aucune fuite), ce qui donne des performances réalistes (AUC ≈ 0,74) plutôt qu'un AUC artificiel de 1,0.

---

##  Schéma d'Architecture du Pipeline

Le système s'articule autour d'une architecture modulaire qui transforme les données transactionnelles et d'expérience brute en indicateurs stratégiques et prédictions actionnables :


```
              ┌─────────────────────────────────────┐
              │   5 SOURCES OLIST (enrichissement)  │
              │ orders+customers+reviews+items+pay  │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │   AUDIT, NETTOYAGE & WINSORISATION   │
              │  (clé customer_unique_id, no leak)   │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │  FEATURE ENG. + 3 MODÈLES + TUNING   │
              │  (Scikit-Learn, XGBoost, SHAP)       │
              └──────────────────┬──────────────────┘
                                 │
                                 ▼
              ┌─────────────────────────────────────┐
              │   artifacts/ (modèle + KPIs + SHAP)  │
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
              │(Dir/Mkt/Ops/Tech)│   │ (MODÈLE RÉEL ML) │
              └──────────────────┘   └──────────────────┘

```


##  Description des Fichiers du Dépôt

* **`notebook_analyse_decisionnelle.ipynb`** : Le Notebook Jupyter principal. Il télécharge automatiquement le dataset Olist (via `kagglehub`), réalise l'audit des données, l'EDA, **quatre** tests statistiques ($t\text{-test}$, Mann-Whitney, $\chi^2$, ANOVA), le clustering $K\text{-Means}$ (choix de $k$ par silhouette), l'entraînement comparatif des 3 modèles avec **tuning des hyperparamètres**, et l'interprétabilité **SHAP** (globale + locale).
* **`app.py`** : L'application **Streamlit** (5 vues). Le simulateur et la liste d'alerte appellent le **modèle réel** chargé depuis `artifacts/`.
* **`artifacts/`** : Modèle entraîné (`churn_model.joblib`), KPIs (`kpis.json`), profils de segments, importances SHAP et tableau comparatif — générés par le notebook et consommés par le dashboard.
* **`requirements.txt`** : Dépendances Python épinglées pour la reproductibilité.
* **`A_B_Testing_Plan.md`** : Plan d'expérimentation A/B pour valider l'impact des recommandations de rétention.

---

##  Instructions d'Installation et Lancement

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

1. **Vue Direction (Stratégique)** : KPIs mesurés (taux d'insatisfaction, retard de livraison, AUC, ROI) et tableau comparatif des modèles.
2. **Vue Marketing (Segmentation)** : Profils réels des segments K-Means et identification du segment prioritaire.
3. **Vue Opérations (Liste d'Alerte)** : Commandes à risque scorées par le **modèle XGBoost réel** pour des actions prioritaires.
4. **Vue Technique (SHAP Importance)** : Importances globales réelles (valeurs |SHAP| moyennes).
5. **Simulateur de Risque en Direct** : Ajustement du profil d'une commande pour obtenir le score du **modèle réel** (`predict_proba`) en temps réel.
