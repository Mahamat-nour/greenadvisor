import pandas as pd

def load_internal_data(path="data/internal_data.xlsx"):
    try:
        electricity = pd.read_excel(path, sheet_name="electricity")
        transport = pd.read_excel(path, sheet_name="transport")
        activity_log = pd.read_excel(path, sheet_name="activity_log")
        return electricity, transport, activity_log
    except Exception as e:
        print(f"Erreur de chargement des données : {e}")
        return None, None, None
