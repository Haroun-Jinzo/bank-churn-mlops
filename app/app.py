import streamlit as st
import requests
import json

# Configuration de la page
st.set_page_config(
    page_title="Bank Churn Predictor",
    page_icon="🏦",
    layout="centered"
)

# Titre et En-tête
st.title("🏦 Prédiction de Churn Bancaire")
st.markdown("---")

# Sidebar pour la configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    # L'URL de votre API Azure (pré-remplie avec la vôtre)
    api_url = st.text_input(
        "URL de l'API Azure",
        value="https://bank-churn.redpond-3c4969cd.spaincentral.azurecontainerapps.io/predict"
    )
    st.info("Cette application interroge votre modèle ML hébergé sur Azure.")

# Formulaire de saisie (Organisation en colonnes pour faire joli)
col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=600)
    age = st.number_input("Âge", min_value=18, max_value=100, value=40)
    tenure = st.number_input("Années client (Tenure)", min_value=0, max_value=10, value=3)
    balance = st.number_input("Solde du compte (€)", min_value=0.0, value=60000.0)

with col2:
    products = st.slider("Nombre de produits", 1, 4, 2)
    salary = st.number_input("Salaire Estimé (€)", min_value=0.0, value=50000.0)
    has_card = st.checkbox("Possède une carte de crédit ?", value=True)
    is_active = st.checkbox("Membre Actif ?", value=True)

# Gestion spéciale pour la Géographie (Menu déroulant -> One Hot Encoding)
location = st.selectbox("Pays de résidence", ["France", "Allemagne", "Espagne"])

# Logique de transformation pour l'API (One-Hot Encoding)
geo_germany = 1 if location == "Allemagne" else 0
geo_spain = 1 if location == "Espagne" else 0
# Si France: germany=0, spain=0 (c'est le comportement par défaut du modèle)

# Bouton de prédiction
if st.button("🚀 Lancer la prédiction", type="primary"):
    
    # Préparation des données (payload)
    input_data = {
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": products,
        "HasCrCard": 1 if has_card else 0,
        "IsActiveMember": 1 if is_active else 0,
        "EstimatedSalary": salary,
        "Geography_Germany": geo_germany,
        "Geography_Spain": geo_spain
    }

    # Appel à l'API
    try:
        with st.spinner('Interrogation de l\'IA sur Azure...'):
            response = requests.post(api_url, json=input_data)
        
        # Affichage du résultat
        if response.status_code == 200:
            result = response.json()
            prob = result['churn_probability']
            risk = result['risk_level']
            
            st.markdown("---")
            st.subheader("Résultat de l'analyse")
            
            # Affichage visuel avec des couleurs
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.metric("Probabilité de départ", f"{prob:.1%}")
            
            with col_res2:
                if risk == "High":
                    st.error(f"Risque : ÉLEVÉ ({risk}) 🚨")
                else:
                    st.success(f"Risque : FAIBLE ({risk}) ✅")
            
            # Debug (optionnel, pour montrer le JSON reçu)
            with st.expander("Voir la réponse brute de l'API"):
                st.json(result)
                
        else:
            st.error(f"Erreur API ({response.status_code}) : {response.text}")
            
    except Exception as e:
        st.error(f"Erreur de connexion : {str(e)}")