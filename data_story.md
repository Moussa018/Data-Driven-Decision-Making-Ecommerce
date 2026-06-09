# Data Story : Anticiper l'Insatisfaction Client pour Fidéliser
*Présentation Exécutive — Data-Driven Decision Making (E-Commerce Olist)*

> Version courte (8 slides, 5–7 minutes) — alignée sur `presentation.tex`.

---

## Slide 1 : Titre
**Anticiper l'Insatisfaction Client pour Fidéliser**
- Data-Driven Decision Making — E-Commerce (Dataset Olist)
- Mohammed Nour Moussa & Mohamed Yassine Reghioui Hamzaoui
- Encadrant : Pr. Y. Tabii — ENSIAS, 2025/2026

---

## Slide 2 : Le Problème — Fidéliser sur une Marketplace
**Le défi de la rétention e-commerce**
- Acquérir un client coûte **5× plus cher** que le retenir.
- Sur Olist, **plus de 97 %** des clients n'achètent **qu'une seule fois** → modéliser le « churn » classique (ré-achat) est **impossible**.
- **Pivot stratégique** : agir *avant* la perte, en prédisant le **risque d'expérience négative** (avis ≤ 2/5), qui est le signal avancé de l'attrition.
- **Question centrale** : *Comment repérer une commande à risque avant que le client ne publie un avis négatif, pour le retenir de façon proactive ?*
- Chiffre d'ancrage : **12,77 %** des commandes finissent en insatisfaction.

---

## Slide 3 : L'Insight — La Livraison Décide de Tout
**Ce qui génère l'insatisfaction**
- **Découverte majeure** : un **retard de livraison** multiplie par **~7** le risque d'insatisfaction.
  - Commande livrée à l'heure → **9 %** d'insatisfaction.
  - Commande livrée en retard → **62 %** d'insatisfaction.
- Le facteur n°1 est l'**écart entre la date promise et la livraison réelle** (`delay_vs_estimate`).
- Confirmé par **4 tests statistiques** (t-test, Mann-Whitney, Chi-deux, ANOVA), tous avec *p ≪ 0,001*.
- C'est un levier **directement actionnable** par l'entreprise.

---

## Slide 4 : La Solution — Une IA + un Outil de Décision
**De la donnée brute à l'action**
- **1. Un modèle prédictif (XGBoost)** :
  - Score chaque commande **en temps réel**.
  - Fiable et réaliste : détecte **plus d'un client insatisfait sur deux**.
  - **Transparent** (valeurs SHAP) : on sait *pourquoi* une commande est signalée.
- **2. Un dashboard décisionnel (Streamlit)** : 5 vues métier — Direction, Marketing, Opérations, Technique, Simulateur en direct.
- **Chaîne de valeur** : Données Olist (5 sources, 95 809 commandes) → Modèle IA (score de risque) → Action (coupon / alerte ciblée).

---

## Slide 5 : 3 Recommandations Actionnables
**Transformer l'insatisfaction en fidélité**
1. **Rétention proactive (immédiat)** : déclencher automatiquement un coupon de 10 % dès que le risque prédit dépasse 50 %.
2. **Refonte logistique (moyen terme)** : renégocier les transporteurs responsables des retards critiques (segment défaillant).
3. **Estimations réalistes (rapide)** : ajuster les délais annoncés sur le site pour éliminer l'effet de déception.
- **À valider scientifiquement** : un A/B test sur 30 jours doit mesurer une baisse significative (*p < 0,05*) du churn sur le groupe « coupon ».

---

## Slide 6 : L'Impact — Le Ciblage par l'IA est Décisif
**Le business case data-driven**
| Indicateur | Valeur |
| :--- | :--- |
| Taux d'insatisfaction | 12,77 % |
| Gain net (campagne ciblée) | **+6 549 €** |
| Retour sur investissement (ROI) | **+20 %** |
- **Le message clé** : sans ciblage, envoyer des coupons à tout le monde génère des **pertes sèches**.
- C'est **l'IA qui rend l'opération rentable**, en ne ciblant que les commandes réellement à risque.

---

## Slide 7 : Conclusion & Prochaines Étapes
**Du POC à la production**
- **Bilan** : nous avons prouvé qu'un système **automatisé, transparent et rentable** peut anticiper l'insatisfaction et retenir les clients — sans gaspiller le budget marketing.
- **Prochaines étapes** :
  1. Lancer l'A/B test sur les 30 prochains jours.
  2. Intégrer la prédiction au CRM (déclenchement automatique des emails).
  3. Suivre la dérive du modèle (*model drift*) mensuellement.

---

## Slide 8 : Questions & Réponses
**Merci de votre attention !**
*Nous sommes à votre disposition pour détailler le modèle, le ROI ou le dashboard.*
