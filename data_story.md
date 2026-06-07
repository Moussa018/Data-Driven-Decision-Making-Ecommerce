# Data Story : Système Prédictif du Risque d'Insatisfaction E-Commerce
*Présentation Exécutive - Décision Data-Driven*

---

## Slide 1 : Introduction
**Projet Data-Driven Decision Making**
- **Sujet** : E-commerce (Dataset Olist)
- **Objectif** : Construire un système d'aide à la décision pour anticiper et réduire l'insatisfaction client.
- **Pourquoi ?** L'insatisfaction est le premier moteur de l'attrition (Churn) et de la perte de chiffre d'affaires.

---

## Slide 2 : Contexte Métier & Problématique
**Le défi de la fidélisation e-commerce**
- **Observation** : Dans notre marché (Olist), >97% des clients sont des acheteurs uniques. 
- **Problème** : Modéliser le "churn" classique est impossible (taux de ré-achat quasi nul).
- **Pivot Stratégique** : Nous devons agir *avant* la perte du client en prédisant le **risque d'expérience client négative** (note ≤ 2/5).
- **Question Centrale** : *Comment identifier une commande à risque avant que le client ne publie un avis négatif pour le retenir de manière proactive ?*

---

## Slide 3 : KPIs & Objectifs
**Mesurer la performance à tous les niveaux**
- **KPI Stratégique** : Marge nette sauvée (ROI des campagnes de rétention).
- **KPIs Opérationnels** :
  - Taux d'insatisfaction global constaté : **12,77%**
  - Taux de commandes livrées en retard : **6,66%**
- **KPIs Techniques** : AUC-ROC (Précision globale) et Rappel (Capacité à détecter tous les clients à risque).

---

## Slide 4 : L'Audit des Données
**Un socle robuste pour nos algorithmes**
- **Sources** : 5 tables distinctes combinées (Commandes, Clients, Avis, Produits, Paiements).
- **Volume** : Plus de 95 000 commandes analysées.
- **Qualité** : 
  - Nettoyage rigoureux et winsorisation des valeurs extrêmes.
  - Aucune fuite de données (Data Leakage) : toutes nos variables explicatives sont strictement connues *avant* la rédaction de l'avis client.

---

## Slide 5 : Ce qui génère l'insatisfaction
**Analyse Exploratoire (EDA)**
- **Découverte Majeure** : L'expérience de livraison est le déclencheur n°1 des avis négatifs.
- **Métriques clés** :
  - Les délais de livraison réels (`delivery_days`).
  - L'écart par rapport à la date estimée (`delay_vs_estimate`).
- Les tests statistiques (t-test, ANOVA) confirment l'impact significatif du retard sur la chute de la satisfaction.

---

## Slide 6 : Segmentation Client
**Comprendre nos profils d'acheteurs**
- Un clustering (K-Means) a permis d'identifier des groupes distincts de comportements d'achat.
- **Le Segment Critique** : Un segment spécifique regroupe les clients victimes de défaillances logistiques (délais explosés, retards systématiques). C'est notre cible prioritaire pour la rétention.

---

## Slide 7 : L'Intelligence Artificielle au Service de l'Action
**Modélisation Prédictive**
- **Choix Technologique** : Évaluation de 3 algorithmes de Machine Learning avec tuning complet des hyperparamètres.
- **Gagnant** : XGBoost.
- **Performance** : 
  - **AUC-ROC** : 0,7437 (Prédictions fiables et réalistes).
  - **Rappel (Recall)** : 0,5353 (Identification de plus de 53% des clients réellement insatisfaits).

---

## Slide 8 : Interprétabilité (La "Boîte de Verre")
**Pourquoi l'IA prend-elle cette décision ?**
- L'utilisation des valeurs **SHAP** nous permet de comprendre chaque prédiction.
- **Au niveau global** : Le modèle confirme que les délais de livraison et le montant des frais de port (Fret) pèsent le plus lourd dans la décision.
- **Au niveau local** : Pour chaque commande bloquée, nos équipes savent *exactement* quelle variable a déclenché l'alerte.

---

## Slide 9 : Le Dashboard Décisionnel
**De la donnée brute à l'outil métier**
- Déploiement d'une application **Streamlit** multi-profils (5 vues) :
  1. **Direction** : Vue macro des KPIs (Taux d'insatisfaction, ROI).
  2. **Marketing** : Profils de segmentation.
  3. **Opérations** : Liste d'alerte des commandes scorées "à haut risque".
  4. **Technique** : Importances SHAP.
  5. **Simulateur en Direct** : Testez une commande et obtenez la probabilité d'insatisfaction en temps réel.

---

## Slide 10 : Recommandations Stratégiques
**3 Actions pour transformer l'insatisfaction en fidélité**
1. **Rétention Proactive (Action Immédiate)** : Déclencher l'envoi d'un coupon de 10% pour toute commande dont le risque prédit par l'IA dépasse 50%.
2. **Refonte Logistique (Action Moyen Terme)** : Renégocier les contrats des transporteurs affiliés au segment générant le plus de retards (`delay_vs_estimate` critique).
3. **Optimisation des Estimations (Action Rapide)** : Ajuster les délais estimés annoncés au client sur le site pour éviter l'effet de déception.

---

## Slide 11 : A/B Testing - Prouver la Valeur
**Validation scientifique des recommandations**
- **Objectif** : Mesurer l'impact de l'envoi du coupon de réduction automatisé (Recommandation 1).
- **Durée** : 30 jours continus.
- **Échantillon cible** : 2 960 clients identifiés à haut risque par XGBoost (1480 en groupe de contrôle, 1480 avec coupon).
- **Critère de Succès** : Réduction statistiquement significative (p-value < 0.05) de 5 points du taux d'attrition.

---

## Slide 12 : Impact Financier & ROI
**Le Business Case Data-Driven**
- En ciblant de manière précise les clients en souffrance avec notre modèle prédictif :
  - **Taux d'insatisfaction** : 12,77% du volume.
  - **Gain Net Estimé** : + 6 549,0 € par campagne ciblée (en déduisant les coûts d'envoi des coupons).
  - **Retour sur Investissement (ROI)** : **20,0 %**
- *Sans le ciblage IA, envoyer des coupons à tout le monde générerait des pertes sèches.*

---

## Slide 13 : Conclusion & Prochaines Étapes
**Du POC (Proof of Concept) à la Production**
- **Bilan** : Nous avons prouvé qu'un système automatisé, transparent et réaliste peut retenir nos clients de manière rentable.
- **Next Steps** :
  1. Lancement de l'A/B test sur les 30 prochains jours.
  2. Intégration de l'API de prédiction dans notre CRM pour déclencher l'envoi des emails.
  3. Suivi mensuel des dérives potentielles du modèle (Model Drift).

---

## Slide 14 : Questions & Réponses
**Merci pour votre attention !**
*Nous sommes à votre disposition pour détailler l'architecture technique, le ROI ou l'interface du Dashboard.*
