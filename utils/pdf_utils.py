import streamlit as st
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

# --- Fonction PDF ---
def clean_text(text):
    return re.sub(r'[^\x00-\xFF]', '', text)

def create_pdf(recos, df_emissions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    if os.path.exists("assets/logo.png"):
        pdf.image("assets/logo.png", x=80, w=50)

    pdf.set_font("Arial", "B", size=16)
    pdf.ln(70)
    pdf.cell(200, 10, txt="GreenAdvisor", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Rapport d'impact carbone", ln=True, align="C")
    pdf.ln(10)

    today = datetime.today()
    date_str = format_date(today, locale="fr_FR")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date : {date_str}", ln=True, align="C")

    pdf.ln(20)
    pdf.set_font("Arial", "I", size=11)
    pdf.multi_cell(0, 8, clean_text(
        "Ce rapport présente une analyse des émissions de CO₂ internes de votre entreprise. "
        "Il inclut une visualisation des postes d'émission les plus significatifs ainsi que des recommandations personnalisées pour les réduire."
    ))

    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, txt="Visualisation des émissions", ln=True, align="L")

    fig, ax = plt.subplots()
    ax.bar(df_emissions["Catégorie"], df_emissions["Émissions (kg CO₂)"], color="seagreen")
    ax.set_ylabel("Émissions (kg CO₂)")
    ax.set_title("Répartition par catégorie")

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    img_path = os.path.join(tempfile.gettempdir(), "emissions_chart.png")
    with open(img_path, "wb") as f:
        f.write(img_buffer.getbuffer())
    plt.close(fig)

    pdf.image(img_path, x=25, w=160)
    pdf.ln(10)

    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, txt="Détail des émissions", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    for idx, row in df_emissions.iterrows():
        text = f"- {row['Catégorie']} : {row['Émissions (kg CO₂)']:.2f} kg"
        pdf.cell(200, 8, txt=clean_text(text), ln=True)

    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, txt="Recommandations personnalisées", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    for reco in recos:
        pdf.multi_cell(0, 8, clean_text(f"• {reco}"))
        pdf.ln(2)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name



if st.button("Exporter le rapport PDF"):
    pdf_path = create_pdf(recos, df_all)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Télécharger le rapport",
            data=f,
            file_name="rapport_greenadvisor.pdf",
            mime="application/pdf"
        )
