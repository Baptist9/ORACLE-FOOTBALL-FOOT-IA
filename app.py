app_code = """
import streamlit as st
import pandas as pd
import joblib
import os

# Configuration de la page
st.set_page_config(page_title="Oracle Football IA", layout="wide")

st.title("⚽ Mon Oracle Football")

# Chargement du modèle avec mise en cache pour éviter de le recharger à chaque interaction
@st.cache_resource
def load_model():
    if os.path.exists('oracle_football_v1.pkl'):
        try:
            return joblib.load('oracle_football_v1.pkl')
        except Exception as e:
            st.error(f"Erreur lors du chargement du modèle : {e}")
            return None
    return None

model = load_model()

if model:
    st.success("✅ IA Prête (Précision estimée : 92.71%)")
else:
    st.warning("⚠️ Modèle 'oracle_football_v1.pkl' introuvable. Veuillez le charger à la racine du projet.")

# Chargement des données avec mise en cache
@st.cache_data
def load_data(url):
    try:
        # dayfirst=True est important pour les formats de date européens (JJ/MM/AAAA)
        df = pd.read_csv(url, parse_dates=['Date'], dayfirst=True)
        return df
    except Exception as e:
        return None

st.subheader("📅 Prochains Matchs à Analyser")

# URL du calendrier (Exemple : Ligue 2 2025/2026)
url = "https://www.football-data.co.uk/mmz4281/2526/F2.csv"
df = load_data(url)

if df is not None:
    try:
        # Vérification que la colonne 'FTR' (Full Time Result) existe
        if 'FTR' in df.columns:
            # Filtrer les matchs à venir (ceux qui n'ont pas encore de résultat)
            fixtures = df[df['FTR'].isnull()].copy()
            
            if not fixtures.empty:
                # Formatage de la date pour l'affichage
                fixtures['Date'] = fixtures['Date'].dt.strftime('%d/%m/%Y')
                
                # Affichage des 10 prochains matchs
                st.table(fixtures[['Date', 'HomeTeam', 'AwayTeam']].head(10))
            else:
                st.info("Aucun match à venir trouvé dans le fichier actuel.")
        else:
            st.error("Le fichier de données ne contient pas la colonne 'FTR' nécessaire.")
    except Exception as e:
        st.error(f"Erreur lors du traitement du calendrier : {e}")
else:
    st.info("Impossible de récupérer le calendrier. Vérifiez votre connexion internet ou l'URL.")
"""

# Écriture du fichier app.py
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ Fichier 'app.py' généré avec succès. Voici le contenu :\n")
print(app_code)
