import json
import os

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data-Driven Decision Dashboard", layout="wide")
st.title("Système d'Aide à la Décision — Risque d'Insatisfaction Client (E-Commerce)")

ART = os.path.join(os.path.dirname(__file__), "artifacts")


@st.cache_resource
def load_artifacts():
    """Charge le modèle réel et les artefacts produits par le notebook."""
    bundle = joblib.load(os.path.join(ART, "churn_model.joblib"))
    kpis = json.load(open(os.path.join(ART, "kpis.json")))
    segments = pd.read_csv(os.path.join(ART, "segments.csv"))
    importance = pd.read_csv(os.path.join(ART, "feature_importance.csv"))
    comparison = pd.read_csv(os.path.join(ART, "model_comparison.csv"))
    return bundle, kpis, segments, importance, comparison


try:
    bundle, KPIS, SEGMENTS, IMPORTANCE, COMPARISON = load_artifacts()
    MODEL, SCALER, FEATURES = bundle["model"], bundle["scaler"], bundle["features"]
    ARTIFACTS_OK = True
except Exception as exc:  # pragma: no cover - garde-fou si artefacts absents
    ARTIFACTS_OK = False
    st.error(
        "Artefacts introuvables dans `artifacts/`. Exécutez d'abord "
        "`notebook_analyse_decisionnelle.ipynb` pour générer le modèle.\n\n"
        f"Détail : {exc}"
    )
    st.stop()

# Valeurs médianes par défaut (commande "typique") pour le simulateur.
DEFAULTS = {
    "delivery_days": 10.0,
    "delay_vs_estimate": -12.0,
    "approval_hours": 10.0,
    "freight": 20.0,
    "price": 120.0,
    "payment_value": 140.0,
    "installments": 2.0,
    "n_items": 1.0,
    "freight_ratio": 0.18,
    "reg_AUTRE": 1.0,
    "reg_MG": 0.0,
    "reg_RJ": 0.0,
    "reg_SP": 0.0,
}


def predict_risk(overrides):
    """Construit le vecteur de features réel et renvoie la proba du modèle."""
    row = {f: DEFAULTS.get(f, 0.0) for f in FEATURES}
    row.update({k: v for k, v in overrides.items() if k in row})
    X = pd.DataFrame([row])[FEATURES]
    X_scaled = SCALER.transform(X)
    return float(MODEL.predict_proba(X_scaled)[:, 1][0])


navigation = st.sidebar.radio(
    "Navigation Profils",
    ["1. Vue Direction (Stratégique)",
     "2. Vue Marketing (Segmentation)",
     "3. Vue Opérations (Liste d'Alerte)",
     "4. Vue Technique (SHAP Importance)",
     "5. Simulateur de Risque en Direct"],
)

# ----------------------------------------------------------------------------
if navigation == "1. Vue Direction (Stratégique)":
    st.header("Tableau de Bord Stratégique (Direction)")
    st.caption("Indicateurs mesurés sur le jeu de données Olist (≈96k commandes livrées).")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Taux d'Insatisfaction", f"{KPIS['dissatisfaction_rate']:.1%}")
    c2.metric("Taux de Livraison en Retard", f"{KPIS['late_rate']:.1%}")
    c3.metric("AUC-ROC (modèle champion)", f"{KPIS['best_auc']:.3f}")
    c4.metric("ROI estimé de la rétention", f"{KPIS['roi_pct']:.0f} %",
              help=f"Gain net annualisé estimé : {KPIS['gain_net_eur']:,.0f} €")

    st.subheader("Performance comparée des modèles")
    st.dataframe(COMPARISON, use_container_width=True, hide_index=True)
    st.info(
        "Contrairement à une approche naïve avec fuite de données (AUC=1.0), "
        "les performances sont réalistes : le modèle discrimine honnêtement le "
        "risque d'insatisfaction et permet un ciblage rentable."
    )

# ----------------------------------------------------------------------------
elif navigation == "2. Vue Marketing (Segmentation)":
    st.header("Ciblage et Segmentation Client (Marketing)")
    st.write("Segments issus du clustering K-Means (k=3) — chiffres réels :")
    df = SEGMENTS.copy()
    df["Taux_Insatisfaction"] = (df["Taux_Insatisfaction"] * 100).round(1).astype(str) + " %"
    st.dataframe(df, use_container_width=True, hide_index=True)

    worst = SEGMENTS.sort_values("Taux_Insatisfaction", ascending=False).iloc[0]
    st.warning(
        f"**Segment prioritaire : #{int(worst['Segment'])}** — délai de livraison moyen "
        f"{worst['Delai_Livraison']:.0f} j, taux d'insatisfaction {worst['Taux_Insatisfaction']:.0%}. "
        "Action : coupon de rétention ciblé + renforcement SLA transporteur."
    )

# ----------------------------------------------------------------------------
elif navigation == "3. Vue Opérations (Liste d'Alerte)":
    st.header("Liste d'Action Opérationnelle (Équipes Terrain)")
    st.write("Commandes scorées **par le modèle réel** selon leur profil logistique :")

    exemples = pd.DataFrame([
        {"Commande": "ORD_1042", "delay_vs_estimate": 18, "delivery_days": 32, "n_items": 3},
        {"Commande": "ORD_2087", "delay_vs_estimate": 12, "delivery_days": 28, "n_items": 1},
        {"Commande": "ORD_3310", "delay_vs_estimate": 6, "delivery_days": 22, "n_items": 2},
        {"Commande": "ORD_4521", "delay_vs_estimate": -2, "delivery_days": 14, "n_items": 1},
        {"Commande": "ORD_5063", "delay_vs_estimate": -15, "delivery_days": 7, "n_items": 1},
    ])
    exemples["Risque d'Insatisfaction"] = exemples.apply(
        lambda r: f"{predict_risk(r.to_dict()):.1%}", axis=1
    )
    st.table(exemples)
    st.caption("Les probabilités proviennent du modèle XGBoost tuné chargé depuis `artifacts/`.")

# ----------------------------------------------------------------------------
elif navigation == "4. Vue Technique (SHAP Importance)":
    st.header("Explicabilité et Transparence Algorithmique (Équipe Tech)")
    st.write("Importance globale des variables (valeurs |SHAP| moyennes réelles) :")
    top = IMPORTANCE.head(8).set_index("feature")["mean_abs_shap"]
    st.bar_chart(top)
    st.caption("Le retard de livraison (`delay_vs_estimate`) est le premier déclencheur du risque.")

# ----------------------------------------------------------------------------
elif navigation == "5. Simulateur de Risque en Direct":
    st.header("Simulateur Prédictif en Temps Réel")
    st.write("Ajustez le profil d'une commande pour voir le score du **modèle réel**.")

    col1, col2 = st.columns(2)
    with col1:
        delay = st.slider("Retard vs date estimée (jours, >0 = en retard) :", -40, 40, -5)
        delivery = st.slider("Délai de livraison total (jours) :", 1, 45, 12)
        n_items = st.number_input("Nombre d'articles :", min_value=1, max_value=20, value=1)
    with col2:
        freight = st.slider("Frais de port (€) :", 0.0, 100.0, 20.0)
        payment = st.slider("Montant payé (€) :", 10.0, 1000.0, 140.0)
        region = st.selectbox("Région client :", ["AUTRE", "SP", "RJ", "MG"])

    overrides = {
        "delay_vs_estimate": delay,
        "delivery_days": delivery,
        "n_items": n_items,
        "freight": freight,
        "payment_value": payment,
        "freight_ratio": freight / max(payment, 1.0),
        "reg_AUTRE": 1.0 if region == "AUTRE" else 0.0,
        "reg_SP": 1.0 if region == "SP" else 0.0,
        "reg_RJ": 1.0 if region == "RJ" else 0.0,
        "reg_MG": 1.0 if region == "MG" else 0.0,
    }
    score = predict_risk(overrides)
    st.subheader(f"Risque d'Insatisfaction Estimé : {score:.1%}")
    if score > 0.5:
        st.error("ALERTE : commande à très haut risque — déclencher la rétention proactive.")
    elif score > 0.25:
        st.warning("Vigilance : risque modéré, surveiller la livraison.")
    else:
        st.success("Parcours sain : faible risque d'insatisfaction.")
