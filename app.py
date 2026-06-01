
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data-Driven Decision Dashboard", layout="wide")
st.title("Système d'Aide à la Décision - Optimisation du Churn E-Commerce")

# Simulation de données
np.random.seed(42)
tendance_data = pd.DataFrame({
    'Mois': ['Jan', 'Fev', 'Mar', 'Avr', 'Mai'],
    'Taux_Churn': [24.5, 23.1, 21.4, 19.8, 17.2],
    'Chiffre_Affaires': [120000, 125000, 131000, 138000, 145000]
})

# Navigation
navigation = st.sidebar.radio(
    "Navigation Profils",
    ["1. Vue Direction (Stratégique)", 
     "2. Vue Marketing (Segmentation)", 
     "3. Vue Opérations (Liste d'Alerte)", 
     "4. Vue Technique (SHAP Importance)", 
     "5. Simulateur de Churn en Direct"]
)

if navigation == "1. Vue Direction (Stratégique)":
    st.header("Tableau de Bord Stratégique (Direction)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Taux de Churn Actuel", "17.2 %", "-2.6 %")
    col2.metric("Chiffre d'Affaires Mensuel", "145,000 €", "+5,100 €")
    col3.metric("ROI Estimé des Campagnes", "410 %", "+15 %")
    
    st.subheader("Évolution du Churn vs Chiffre d'Affaires")
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.lineplot(data=tendance_data, x='Mois', y='Taux_Churn', marker='o', color='red', ax=ax)
    ax.set_ylabel("Taux de Churn (%)")
    st.pyplot(fig)

elif navigation == "2. Vue Marketing (Segmentation)":
    st.header("Ciblage et Segmentation Client (Marketing)")
    st.write("Répartition des profils issus de la phase de Clustering K-Means :")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Segment : Clients Dormants**\n\n* **Volume :** 45%\n* **Action :** Campagne de réactivation massive par email.")
    with col2:
        st.warning("**Segment : Clients à Risque Insatisfaits**\n\n* **Volume :** 15%\n* **Action :** Appel du service client + Coupon de 15%.")

elif navigation == "3. Vue Opérations (Liste d'Alerte)":
    st.header("Liste d'Action Opérationnelle (Équipes Terrains)")
    st.write("Top des clients prioritaires prédits 'En risque imminent de rupture' par le modèle XGBoost :")
    liste_alerte = pd.DataFrame({
        'ID Client': [f'CLIENT_{i}' for i in range(101, 106)],
        'Probabilité Churn': ['98.4%', '95.1%', '91.2%', '89.7%', '85.3%'],
        'Dernière Note': [1, 1, 2, 1, 2],
        'Jours Inactif': [89, 85, 82, 80, 79]
    })
    st.table(liste_alerte)

elif navigation == "4. Vue Technique (SHAP Importance)":
    st.header("⚙️ Explicabilité et Transparence Algorithmique (Équipe Tech)")
    st.write("Poids des facteurs décisionnels calculés via les valeurs SHAP globales :")
    
    # CORRECTION ICI : Le nom dans la liste correspond exactement au nom dans 'by'
    features_importance = pd.DataFrame({
        'Feature Métier': ['Récence (Jours)', 'Satisfaction (Note)', 'Fréquence (Commandes)'],
        'Importance': [0.65, 0.25, 0.10]
    }).sort_values(by='Importance', ascending=False)
    
    st.bar_chart(data=features_importance, x='Feature Métier', y='Importance')

elif navigation == "5. Simulateur de Churn en Direct":
    st.header(" Simulateur Prédictif en Temps Réel")
    st.write("Modifiez le profil d'un client pour voir l'impact immédiat sur son score de Churn.")
    recence = st.slider("Jours depuis le dernier achat :", 1, 365, 45)
    satisfaction = st.slider("Note de satisfaction moyenne (1 à 5) :", 1.0, 5.0, 4.2)
    commandes = st.number_input("Nombre total de commandes passées :", min_value=1, value=2)
    
    score_simulation = (recence / 365) * 0.7 + (1 - (satisfaction / 5)) * 0.3
    score_final = min(max(score_simulation, 0.0), 1.0)
    
    st.subheader(f"Risque de Churn Estimé : {score_final:.1%}")
    if score_final > 0.5:
        st.error("ALERTE : Client à très haut risque de départ !")
    else:
        st.success("Statut Sain : Client engagé.")
