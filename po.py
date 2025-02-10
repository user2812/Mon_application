import pandas as pd
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup

# ---- CUSTOM CSS ----
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        background-image: url('https://cdn.pixabay.com/photo/2016/11/08/14/43/dumbo-1808477_1280.jpg'); /* Replace with your image URL */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    h1, h2, h3, h4, h5, h6, p, .stMarkdown, .stTextInput, .stButton, .stDownloadButton, .stTextArea {
        color: #000000; /* Change this to the desired text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- TITRE ----
st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

# ---- MENU DE NAVIGATION ----
menu = ["🏠 Accueil", "🔍 Scraper des données", "📥 Télécharger données", "📊 Evaluer l'appli"]
choice = st.sidebar.selectbox("Menu", menu)

st.markdown("""
This app allows you to analyze data from a single CSV file.  
* **Python libraries:** pandas, streamlit  
* **Data source:** [CoinAfrique](https://sn.coinafrique.com/)
""")

# ---- CHARGER LES DONNÉES ----
@st.cache_data
def load_data():
    base_path = "C:/Users/Madame SALL/Drive/Data Collection/My_Data_app/data"
    files = {
        "Chaussures Enfant": os.path.join(base_path, "Chauss_enfant.csv"),
        "Chaussures Homme": os.path.join(base_path, "chaussure_homme.csv"),
        "Vêtements Enfant": os.path.join(base_path, "vetement_enfant.csv"),
        "Vêtements Homme": os.path.join(base_path, "Vet_homme.csv"),
    }
    dataframes = {}
    for name, path in files.items():
        if os.path.exists(path):
            try:
                dataframes[name] = pd.read_csv(path, encoding='ISO-8859-1')
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier {name}: {e}")
                dataframes[name] = pd.DataFrame()  # Crée un DataFrame vide en cas d'erreur
        else:
            st.error(f"⚠️ Fichier introuvable : {path}")
            dataframes[name] = pd.DataFrame()  # Crée un DataFrame vide si le fichier n'existe pas
    return dataframes

if choice == "🏠 Accueil":
    st.subheader("🏠 Accueil")
    st.write("Bienvenue sur My Data App ! Utilisez le menu de gauche pour naviguer.")
    data = load_data()

    # ---- RÉSUMÉ DES DONNÉES ----
    st.subheader("📊 Résumé des données disponibles")
    for name, df in data.items():
        st.write(f"**{name}**: {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # ---- CHOISIR UN FICHIER À AFFICHER ----
    selected_data = st.selectbox("Sélectionnez un dataset :", list(data.keys()))
    df = data[selected_data]

    # ---- AFFICHER LES DONNÉES ----
    st.subheader(f"📊 Aperçu des données : {selected_data}")
    st.write(f"Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    st.dataframe(df)

elif choice == "🔍 Scraper des données":
    st.subheader("🔍 Scraper des données")
    url = st.text_input("Entrer l'URL à scraper", "https://example.com")
    if st.button("Scraper"):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            soup = BeautifulSoup(response.content, "html.parser")
            st.write(soup.prettify())

            # ---- EXTRAIRE LES DONNÉES ----
            data = []
            table = soup.find('table')
            if table:
                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.error("Aucune table trouvée sur la page.")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la requête : {e}")
        except Exception as e:
            st.error(f"Erreur lors du scraping : {e}")

elif choice == "📥 Télécharger données":
    st.subheader("📥 Télécharger données")
    data = load_data()
    selected_data = st.selectbox("Sélectionnez un dataset à télécharger :", list(data.keys()))
    df = data[selected_data]
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les données en CSV",
        data=csv,
        file_name=f"{selected_data}.csv",
        mime='text/csv',
    )

elif choice == "📊 Evaluer l'appli":
    st.subheader("📊 Evaluer l'appli")
    
     # ---- FORMULAIRE D'ÉVALUATION ----
    st.markdown("### Veuillez évaluer l'application")
    rating = st.slider("Notez l'application (1 à 5 étoiles)", 1, 5, 3)
    feedback = st.text_area("Commentaire", "Entrer votre commentaire ici...")
    if st.button("Soumettre"):
        st.success("Merci pour votre commentaire !")
        # ---- ENREGISTRER LE COMMENTAIRE ----
        with open("feedback.txt", "a") as f:
            f.write(feedback + "\n")

# ---- FOOTER ----
st.markdown(
    """
    <footer style='text-align: center; padding: 10px;'>
        <p>© 2025 My Data App. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True
)