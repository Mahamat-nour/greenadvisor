import streamlit as st

st.set_page_config(
    page_title="GreenAdvisor - Analyse Carbone",
    page_icon="🌱",
    layout="wide"
)

import pandas as pd
import requests
import plotly.express as px
import re
import tempfile
import os
from fpdf import FPDF
import unicodedata
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.recommender import estimate_co2_emissions, generate_recommendations
import plotly.io as pio
import matplotlib.pyplot as plt
import io
from datetime import datetime
from babel.dates import format_date
from utils.pdf_utils import create_pdf




# --- Header principal ---
st.markdown("<h1 style='text-align: center; color: #00796B;'>🌱 GreenAdvisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Optimisez votre impact carbone grâce à l'Intelligence Artificielle</p>", unsafe_allow_html=True)

st.markdown("---")

# --- Layout principal ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📂 Importer votre fichier Excel")
    uploaded_file = st.file_uploader("Choisissez un fichier...", type=["xlsx"])

    if uploaded_file:
        try:
            xls = pd.ExcelFile(uploaded_file)
            electricity = pd.read_excel(xls, "electricity")
            transport = pd.read_excel(xls, "transport")
            activity = pd.read_excel(xls, "activity_log")

            electricity, transport, activity = estimate_co2_emissions(electricity, transport, activity)
            recos = generate_recommendations(electricity, transport, activity)

            df_all = pd.DataFrame({
                "Catégorie": ["Électricité", "Transport", "Activité numérique"],
                "Émissions (kg CO₂)": [
                    electricity["emissions_kg"].sum(),
                    transport["emissions_kg"].sum(),
                    activity["emissions_kg"].sum()
                ]
            })

            st.success("✅ Données traitées avec succès.")
            st.write(df_all)

        except Exception as e:
            st.error(f"Erreur lors du traitement des données : {e}")
            st.stop()

        st.subheader("📥 Exporter votre rapport")
        if st.button("Générer le rapport PDF"):
            with st.spinner("Génération du rapport..."):
                pdf_path = create_pdf(recos, df_all)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Télécharger le rapport",
                    data=f,
                    file_name="rapport_greenadvisor.pdf",
                    mime="application/pdf"
                )

with col2:
    st.subheader("📈 Visualisation des émissions")

    if uploaded_file:
        fig = px.bar(
            df_all,
            x="Catégorie",
            y="Émissions (kg CO₂)",
            title="Émissions par catégorie",
            color="Émissions (kg CO₂)",
            color_continuous_scale="Tealgrn"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2025 GreenAdvisor - Propulsé par l'IA durable 🚀</p>", unsafe_allow_html=True)
