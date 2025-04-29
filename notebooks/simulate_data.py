import pandas as pd
import numpy as np

# Crée 30 jours de données
dates = pd.date_range(start="2024-01-01", periods=30)

# Consommation électrique quotidienne
electricity = pd.DataFrame({
    "date": dates,
    "consumption_kwh": np.random.normal(120, 10, size=30).round(2)
})

# Données de transport des employés
transport = pd.DataFrame({
    "employee_id": range(1, 21),
    "distance_km": np.random.uniform(5, 40, size=20).round(1),
    "mode": np.random.choice(["car", "public_transport", "bike", "walk"], size=20, p=[0.5, 0.3, 0.1, 0.1])
})

# Activité numérique quotidienne
activity = pd.DataFrame({
    "date": dates,
    "emails_sent": np.random.poisson(60, size=30),
    "video_calls_hours": np.random.uniform(1, 3, size=30).round(2)
})

# Sauvegarde dans un fichier Excel multi-feuilles
with pd.ExcelWriter("data/internal_data.xlsx") as writer:
    electricity.to_excel(writer, sheet_name="electricity", index=False)
    transport.to_excel(writer, sheet_name="transport", index=False)
    activity.to_excel(writer, sheet_name="activity_log", index=False)








# st.set_page_config(page_title="GreenAdvisor", page_icon="🌿")

# st.title("🌿 GreenAdvisor - Bilan carbone d'entreprise")

# st.markdown("Analyse des émissions internes & recommandations personnalisées.")

# st.header("📤 Charger vos propres données internes")

# uploaded_file = st.file_uploader("Uploader un fichier Excel (.xlsx)", type=["xlsx"])

# if uploaded_file:
#     try:
#         # Lire les feuilles du fichier
#         xls = pd.ExcelFile(uploaded_file)
#         electricity = pd.read_excel(xls, "electricity")
#         transport = pd.read_excel(xls, "transport")
#         activity = pd.read_excel(xls, "activity_log")

#         # Recalculer les émissions localement
#         from app.recommender import estimate_co2_emissions, generate_recommendations
#         electricity, transport, activity = estimate_co2_emissions(electricity, transport, activity)
#         recos = generate_recommendations(electricity, transport, activity)

#         st.success("✅ Données chargées avec succès.")

#     except Exception as e:
#         st.error(f"Erreur de lecture du fichier : {e}")
#         st.stop()
# else:
#     # Si pas de fichier, on fallback sur l'API
#     st.subheader("Ou utilisez les données internes par défaut")
#     try:
#         emissions = requests.get("http://localhost:8000/co2").json()
#         recos = requests.get("http://localhost:8000/recommendations").json()["recommendations"]

#         electricity = pd.DataFrame({"source": ["API"], "emissions_kg": [emissions["electricity_kg"]]})
#         transport = pd.DataFrame({"source": ["API"], "emissions_kg": [emissions["transport_kg"]]})
#         activity = pd.DataFrame({"source": ["API"], "emissions_kg": [emissions["activity_kg"]]})

#     except:
#         st.error("⚠️ API non disponible.")
#         st.stop()
        
       
# st.header("📈 Visualisation des émissions")

# df_all = pd.DataFrame({
#     "Catégorie": ["Électricité", "Transport", "Activité numérique"],
#     "Émissions (kg CO₂)": [
#         electricity["emissions_kg"].sum(),
#         transport["emissions_kg"].sum(),
#         activity["emissions_kg"].sum()
#     ]
# })

# fig = px.bar(df_all, x="Catégorie", y="Émissions (kg CO₂)", color="Catégorie", title="Répartition des émissions")
# st.plotly_chart(fig, use_container_width=True)