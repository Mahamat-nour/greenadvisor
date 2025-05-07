#import sys
#import os

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from data_loader import load_internal_data
from recommender import estimate_co2_emissions, generate_recommendations

app = FastAPI(title="GreenAdvisor API", version="0.1")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API GreenAdvisor 🚀"}

@app.get("/co2")
def get_emissions():
    electricity, transport, activity = load_internal_data()
    electricity, transport, activity = estimate_co2_emissions(electricity, transport, activity)

    total = {
        "electricity_kg": round(electricity["emissions_kg"].sum(), 2),
        "transport_kg": round(transport["emissions_kg"].sum(), 2),
        "activity_kg": round(activity["emissions_kg"].sum(), 2),
        "total_kg": round(
            electricity["emissions_kg"].sum() +
            transport["emissions_kg"].sum() +
            activity["emissions_kg"].sum(), 2
        )
    }

    return total

@app.get("/recommendations")
def get_recommendations():
    electricity, transport, activity = load_internal_data()
    electricity, transport, activity = estimate_co2_emissions(electricity, transport, activity)
    recommendations = generate_recommendations(electricity, transport, activity)

    return {"recommendations": recommendations}
