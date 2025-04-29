import pandas as pd

def estimate_co2_emissions(electricity, transport, activity_log):
    # Émissions liées à l’électricité
    electricity["emissions_kg"] = electricity["consumption_kwh"] * 0.056
    
    # Transport domicile-travail
    def get_transport_emission(row):
        if row["mode"] == "car":
            return row["distance_km"] * 2 * 0.2
        elif row["mode"] == "public_transport":
            return row["distance_km"] * 2 * 0.035
        else:
            return 0
    
    transport["emissions_kg"] = transport.apply(get_transport_emission, axis=1)

    # Activité numérique
    activity_log["emissions_kg"] = (
        activity_log["emails_sent"] * 0.00002 +
        activity_log["video_calls_hours"] * 0.15
    )

    return electricity, transport, activity_log

# 🧠 Étape 4 : Génération de recommandations personnalisées

def generate_recommendations(electricity, transport, activity_log):
    recommendations = []

    # Électricité
    mean_kwh = electricity["consumption_kwh"].mean()
    if mean_kwh > 130:
        recommendations.append("⚡ Réduire la consommation électrique : installer des minuteurs, passer à l’éclairage LED, et couper les équipements hors horaires.")

    # Transport
    car_ratio = (transport["mode"] == "car").sum() / len(transport)
    if car_ratio > 0.5:
        recommendations.append("🚗 Inciter au covoiturage ou aux transports en commun via des primes, forfait mobilité durable ou des abonnements pris en charge.")

    # Activité numérique
    mean_visio = activity_log["video_calls_hours"].mean()
    mean_emails = activity_log["emails_sent"].mean()

    if mean_visio > 2.5:
        recommendations.append("💻 Réduire l’impact des visioconférences : couper la webcam par défaut ou préférer les réunions audio pour les points simples.")

    if mean_emails > 80:
        recommendations.append("📧 Encourager l’utilisation de canaux internes type chat ou outils collaboratifs (Slack, Teams) pour limiter les envois d’emails inutiles.")

    if not recommendations:
        recommendations.append("✅ Très bon comportement global. Continuer à suivre les émissions régulièrement pour ajuster les actions.")

    return recommendations
