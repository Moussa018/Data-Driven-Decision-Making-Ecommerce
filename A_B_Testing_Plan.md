#  PROTOCOLE EXPÉRIMENTAL : PLAN D'A/B TESTING
**Optimisation de la Rétention Client via Coupons de Réduction Ciblés**

---

## 1. Cadrage Stratégique & Hypothèses

L'analyse exploratoire et la modélisation prédictive ont mis en évidence que **l'expérience de livraison** (`delay_vs_estimate`, `delivery_days`) est le déclencheur n°1 de l'**insatisfaction client** (note ≤ 2), elle-même signal avancé majeur de l'attrition (Churn). Le modèle XGBoost (AUC ≈ 0,74, rappel ≈ 0,54) permet de **flaguer en temps réel les commandes à haut risque d'insatisfaction**.

Pour traduire ces insights en valeur économique, nous mettons en place un plan d'A/B Testing standardisé visant à valider l'impact d'une campagne incitative de rétention déclenchée sur ce segment à risque.

### 1.1 Formulations des Hypothèses Statistiques
* **Hypothèse Nulle ($H_0$) :** L'attribution automatisée d'un coupon de réduction de 10% aux clients dont la commande est prédite "à haut risque d'insatisfaction" par le modèle XGBoost n'a aucun effet significatif sur le taux de churn à 30 jours.
$$\text{Taux de Churn}_{\text{Groupe A}} = \text{Taux de Churn}_{\text{Groupe B}}$$

* **Hypothèse Alternative ($H_1$) :** L'attribution automatisée d'un coupon de réduction de 10% aux clients prédits "à haut risque" par le modèle XGBoost réduit de manière statistiquement significative le taux de churn à 30 jours.
$$\text{Taux de Churn}_{\text{Groupe B}} < \text{Taux de Churn}_{\text{Groupe A}}$$

---

## 2. Protocole d'Échantillonnage & Paramètres du Test

### 2.1 Définition de la Population Cible
Le test cible exclusivement les commandes dont le **score de risque d'insatisfaction** calculé par le modèle XGBoost dépasse le seuil opérationnel retenu (par défaut **≥ 50%**, ajustable selon l'arbitrage précision/rappel), c'est-à-dire le segment logistique défaillant identifié lors du clustering (délai et retard de livraison élevés).

### 2.2 Constitution des Groupes
Dès qu'un client franchit le seuil d'alerte, il est assigné de manière aléatoire et uniforme (Randomized Assignment) à l'un des deux groupes :
* **Groupe A (Groupe Témoin - 50% de l'échantillon) :** Ce groupe subit le parcours utilisateur standard. Aucune communication spécifique, aucun coupon de réduction ne lui est envoyé.
* **Groupe B (Groupe Test - 50% de l'échantillon) :** Ce groupe reçoit un email transactionnel automatisé déclenché en temps réel, contenant un code promotionnel de 10% de réduction valable sur l'ensemble du catalogue pendant 14 jours.

### 2.3 Calcul de la Taille de l'Échantillon & Durée
Pour garantir la validité des conclusions mathématiques et éviter les faux positifs, les paramètres de puissance statistique sont fixés selon les standards de l'industrie :
* **Niveau de signification ($\alpha$) :** $5\%$ (probabilité de rejeter $H_0$ alors qu'elle est vraie).
* **Puissance statistique ($1 - \beta$) :** $80\%$ (probabilité de détecter un effet s'il existe réellement).
* **Taux de Churn de base constaté (Baseline) :** $20\%$.
* **Effet Minimum Détectable (MDE) :** Baisse de $5$ points de pourcentage (passer de $20\%$ à $15\%$).

D'après le calcul de taille d'échantillon pour la comparaison de deux proportions indépendantes, la taille minimale requise est de **1 480 clients par groupe**, soit un échantillon global de **2 960 clients**.

Given le volume de notre dataset historique ($> 50 000$ lignes), le flux de clients entrant dans la zone de risque permet de collecter cet échantillon sur une **durée stricte de 30 jours**.

---

## 3. Métriques de Suivi & Critères de Succès

### 3.1 Métriques Primaires (Performance)
* **Taux de Churn à 30 jours :** Nombre de clients n'ayant pas passé commande à l'issue de la fenêtre d'observation / Nombre total de clients du groupe.

### 3.2 Métriques Secondaires (Santé Économique)
* **Taux de Conversion du Coupon :** Pourcentage de clients du Groupe B ayant utilisé le code promo.
* **Valeur Moyen de la Commande (AOV) :** Vérifier si le coupon n'a pas artificiellement détruit la marge unitaire.

### 3.3 Test Statistique de Validation
À l'échéance des 30 jours, l'écart de proportion constaté entre le Groupe A et le Groupe B sera soumis à un **Test du Chi-deux ($\chi^2$) d'indépendance**. 

La décision business de déployer l'algorithme à grande échelle sera validée si et seulement si la **$p\text{-value}$ calculée est inférieure à $0,05$**, confirmant que la baisse du churn est mathématiquement imputable à l'action marketing et non au hasard.

---

## 4. Analyse d'Impact & ROI Prévisionnel

Si le critère de succès statistique est validé (baisse du churn de 5 points de pourcentage sur la population ciblée), l'impact financier est modélisé ainsi. **Point méthodologique clé :** le coût d'incitation doit compter **tous les coupons envoyés** au groupe ciblé, et non seulement ceux qui sont utilisés — c'est l'erreur qui gonflait artificiellement le ROI à +900 % dans une version antérieure.

| Indicateur Financier | Formule de Calcul | Valeur Estimée |
| :--- | :--- | :--- |
| Population ciblée (à risque, /an) | $100 000 \text{ commandes} \times 12{,}8\% \text{ (taux d'insatisfaction mesuré)}$ | $\approx 12\,800 \text{ ciblés}$ |
| Volume de Rétention (MDE 5 pts) | $12\,800 \times 5\%$ | $640 \text{ clients sauvés}$ |
| Chiffre d'Affaires Brut Sauvé | $640 \times 50€ \text{ (marge moyenne)}$ | **$+32\,000 €$** |
| Coût de l'incitation (coupons **envoyés**) | $12\,800 \times 5€$ | $-64\,000 €$ |
| **Gain Net** | $32\,000€ - 64\,000€$ | **$-32\,000 €$** |

> Avec un envoi indifférencié à tout le segment, l'opération est **déficitaire** : c'est précisément pourquoi le **ciblage par le modèle** (rappel ≈ 0,54, score ≥ seuil) est indispensable pour ne couponner que les commandes réellement à risque et atteindre un ROI positif. Le calcul détaillé et data-driven du ROI net figure dans la cellule *« Business Case chiffré »* du notebook (`notebook_analyse_decisionnelle.ipynb`), qui dérive l'ensemble des paramètres des chiffres réellement observés.
